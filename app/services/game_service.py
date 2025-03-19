import uuid
import json
from datetime import datetime
from flask_login import current_user
from app import db
from app.models import GameSession, User
from game_logic.card_package import Deck, Card, Suit, Rank
from game_logic.players import Player
from game_logic.game_management.game import DurakGameManager

# Dictionary to store active games in memory
# In a production app, this would be in Redis or another external store
ACTIVE_GAMES = {}

class GameService:
    """Service that connects game logic to the web application"""
    
    @staticmethod
    def create_ai_game(user_id):
        """Create a new game against AI"""
        # Get user
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Create players
        human_player = Player(f"Player_{user_id}")
        ai_player = Player("AI_Opponent")
        
        # Create game
        game_manager = DurakGameManager(player1=human_player, player2=ai_player)
        
        # Generate unique game ID
        game_id = str(uuid.uuid4())
        
        # Store game state in database - ensure we store players as a simple string
        # to avoid SQLite datatype issues
        game_session = GameSession(
            id=game_id,
            players=f"{user_id},AI",  # Use simple string format instead of JSON
            game_state="ongoing",
            is_against_ai=True,
            start_time=datetime.utcnow()
        )
        
        try:
            db.session.add(game_session)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving game session: {str(e)}")
            # Continue anyway since we'll keep the game in memory
        
        # Store game manager in memory
        ACTIVE_GAMES[game_id] = {
            'manager': game_manager,
            'players': {
                str(user_id): human_player,
                'AI': ai_player
            }
        }
        
        # Return serializable game state
        return {
            "game_id": game_id,
            "players": [human_player.name, ai_player.name],
            "trump_card": str(game_manager.trump_card),
            "created_at": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def get_game_state(game_id, user_id):
        """Get the current game state for a specific user"""
        if game_id not in ACTIVE_GAMES:
            # Try to find it in the database
            game_session = GameSession.query.get(game_id)
            if not game_session:
                return {
                    "error": "Game not found",
                    "game_id": game_id
                }
            
            # Return minimal state for now
            return {
                "game_id": game_id,
                "error": "Game is not active in memory, please start a new game"
            }
        
        game_data = ACTIVE_GAMES[game_id]
        game_manager = game_data['manager']
        
        # Get player's hand
        player = game_data['players'].get(str(user_id))
        if not player:
            return {
                "error": f"Player {user_id} is not part of game {game_id}",
                "game_id": game_id
            }
        
        # Find opponent (assuming 2-player game)
        opponent_id = 'AI' if str(user_id) != 'AI' else str(user_id)
        
        # Build state object
        try:
            state = {
                "game_id": game_id,
                "trump_card": str(game_manager.trump_card),
                "hand": [str(card) for card in player.hand],
                "attacker": game_manager.attacker.name,
                "defender": game_manager.defender.name,
                "is_player_turn": (
                    (game_manager.attacker == player and game_manager.turn_manager.is_attacker_turn) or
                    (game_manager.defender == player and game_manager.turn_manager.is_defender_turn)
                ),
                "board": [str(card) for card in game_manager.board_manager.get_board_state()],
                "deck_size": len(game_manager.deck),
                "opponent_hand_size": len(game_data['players'][opponent_id].hand),
            }
            return state
        except Exception as e:
            print(f"Error getting game state: {str(e)}")
            return {
                "error": f"Error getting game state: {str(e)}",
                "game_id": game_id
            }
    
    @staticmethod
    def play_card(game_id, user_id, card_index):
        """Play a card from a player's hand"""
        if game_id not in ACTIVE_GAMES:
            return {"error": f"Game {game_id} not found or not active"}
        
        game_data = ACTIVE_GAMES[game_id]
        game_manager = game_data['manager']
        player = game_data['players'].get(str(user_id))
        
        if not player:
            return {"error": f"Player {user_id} is not part of game {game_id}"}
        
        if card_index < 0 or card_index >= len(player.hand):
            return {"error": f"Invalid card index: {card_index}"}
        
        card = player.hand[card_index]
        
        # Check if it's player's turn
        is_attacker = (game_manager.attacker == player and game_manager.turn_manager.is_attacker_turn)
        is_defender = (game_manager.defender == player and game_manager.turn_manager.is_defender_turn)
        
        if not (is_attacker or is_defender):
            return {"error": "It's not your turn"}
        
        # Execute move based on player role
        try:
            if is_attacker:
                success = game_manager.turn_manager.execute_attack(card)
                if not success:
                    return {"error": "Invalid attack move"}
            else:  # is_defender
                attack_card = game_manager.board_manager.get_board_state()[-1]
                success = game_manager.turn_manager.handle_defense(attack_card, card)
                if not success:
                    return {"error": "Invalid defense move"}
            
            # After move is executed, let AI play if it's AI's turn
            GameService._handle_ai_turn(game_id)
            
            # Return updated game state
            return GameService.get_game_state(game_id, user_id)
        except Exception as e:
            return {"error": f"Error playing card: {str(e)}"}
    
    @staticmethod
    def _handle_ai_turn(game_id):
        """Handle AI's turn if it's AI's turn to play"""
        game_data = ACTIVE_GAMES[game_id]
        game_manager = game_data['manager']
        ai_player = game_data['players']['AI']
        
        # Check if it's AI's turn
        is_ai_attacker = (game_manager.attacker == ai_player and game_manager.turn_manager.is_attacker_turn)
        is_ai_defender = (game_manager.defender == ai_player and game_manager.turn_manager.is_defender_turn)
        
        if not (is_ai_attacker or is_ai_defender):
            return  # Not AI's turn
        
        # Simple AI logic - pick the first valid card
        if is_ai_attacker:
            for i, card in enumerate(ai_player.hand):
                if game_manager.turn_manager.execute_attack(card):
                    break
        else:  # is_ai_defender
            attack_card = game_manager.board_manager.get_board_state()[-1]
            valid_defense_made = False
            for i, card in enumerate(ai_player.hand):
                if game_manager.turn_manager.handle_defense(attack_card, card):
                    valid_defense_made = True
                    break
            
            # If AI can't defend, pick up cards
            if not valid_defense_made:
                # TODO: Implement picking up cards logic
                pass