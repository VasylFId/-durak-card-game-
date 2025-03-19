# app/services/game_service.py

import uuid
import json
from datetime import datetime
from flask_login import current_user
from app.extensions import db  # Import from extensions instead of app
from app.models import GameSession, User
from game_logic.card_package import Deck, Card, Suit, Rank
from game_logic.players.player import Player
from game_logic.game_management.game import DurakGameManager
import logging

logger = logging.getLogger(__name__)

ACTIVE_GAMES = {}

class GameService:
    @staticmethod
    def create_ai_game(user_id):
        logger.info(f"Creating AI game for user ID: {user_id}")
        try:
            user = User.query.get(user_id)
            if not user:
                logger.error(f"User with ID {user_id} not found")
                raise ValueError(f"User with ID {user_id} not found")

            human_player = Player(f"Player_{user_id}")
            ai_player = Player("AI_Opponent")
            logger.info(f"Created players: {human_player.name} and {ai_player.name}")

            logger.info("Initializing game manager...")
            game_manager = DurakGameManager(player1=human_player, player2=ai_player)
            logger.info(f"Game manager initialized with trump card: {game_manager.trump_card}")

            logger.info("Creating database record...")
            game_session = GameSession(
                players=f"{user_id},AI",
                game_state="ongoing",
                is_against_ai=True,
                start_time=datetime.utcnow()
            )
            try:
                db.session.add(game_session)
                db.session.commit()
                game_id = game_session.id
                logger.info(f"Game session saved to database with ID: {game_id}")
            except Exception as e:
                db.session.rollback()
                logger.error(f"ERROR saving game session: {str(e)}")
                raise

            ACTIVE_GAMES[str(game_id)] = {
                'manager': game_manager,
                'players': {
                    str(user_id): human_player,
                    'AI': ai_player
                },
                'session_id': game_id
            }
            logger.info(f"Game state stored in memory with key: {game_id}")

            user.games_against_ai = (user.games_against_ai or 0) + 1
            user.total_games = (user.total_games or 0) + 1
            try:
                db.session.commit()
                logger.info(f"User statistics updated: games_against_ai={user.games_against_ai}, total_games={user.total_games}")
            except Exception as e:
                db.session.rollback()
                logger.error(f"ERROR updating user statistics: {str(e)}")

            result = {
                "game_id": str(game_id),
                "players": [human_player.name, ai_player.name],
                "trump_card": str(game_manager.trump_card),
                "created_at": datetime.utcnow().isoformat()
            }
            logger.info(f"Game created successfully: {result}")
            return result
        except Exception as e:
            logger.error(f"ERROR in create_ai_game: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    # Rest of the GameService class methods remain the same
    # ... (keep all other methods unchanged)

    @staticmethod
    def get_game_state(game_id, user_id=None):
        game_id_str = str(game_id)
        if game_id_str not in ACTIVE_GAMES:
            try:
                game_id_int = int(game_id)
                game_session = GameSession.query.get(game_id_int)
            except (ValueError, TypeError):
                game_session = None
            
            if not game_session:
                return {
                    "error": "Game not found",
                    "game_id": game_id
                }
            
            return {
                "game_id": game_id,
                "error": "Game is not active in memory, please start a new game"
            }
        
        game_data = ACTIVE_GAMES[game_id_str]
        game_manager = game_data['manager']
        
        if user_id:
            player = game_data['players'].get(str(user_id))
            if not player:
                return {
                    "error": f"Player {user_id} is not part of game {game_id}",
                    "game_id": game_id
                }
            
            opponent_id = None
            for pid in game_data['players']:
                if pid != str(user_id):
                    opponent_id = pid
                    break
            
            try:
                if not hasattr(game_manager, 'turn_manager') or game_manager.turn_manager is None:
                    logger.info("Initializing turn_manager which was not found")
                    from game_logic.game_management.turn_manager import TurnManager
                    
                    if hasattr(game_manager, 'board_manager'):
                        game_manager.turn_manager = TurnManager(
                            attacker=game_manager.attacker,
                            defender=game_manager.defender,
                            board_manager=game_manager.board_manager
                        )
                    else:
                        logger.info("board_manager not found, initializing it too")
                        from game_logic.game_management.board_manager import BoardManager
                        game_manager.board_manager = BoardManager(trump_card=game_manager.trump_card)
                        game_manager.turn_manager = TurnManager(
                            attacker=game_manager.attacker,
                            defender=game_manager.defender,
                            board_manager=game_manager.board_manager
                        )
                
                is_player_turn = False
                if hasattr(game_manager, 'turn_manager') and game_manager.turn_manager is not None:
                    is_player_turn = (
                        (game_manager.attacker == player and game_manager.turn_manager.is_attacker_turn) or
                        (game_manager.defender == player and game_manager.turn_manager.is_defender_turn)
                    )
                
                state = {
                    "game_id": game_id,
                    "trump_card": str(game_manager.trump_card),
                    "hand": [str(card) for card in player.hand],
                    "attackerName": game_manager.attacker.name,
                    "defenderName": game_manager.defender.name,
                    "isPlayerTurn": is_player_turn,
                    "board": [str(card) for card in game_manager.board_manager.get_board_state()],
                    "deckSize": len(game_manager.deck),
                    "opponentHandSize": len(game_data['players'][opponent_id].hand) if opponent_id else 0,
                    "isGameOver": GameService._is_game_over(game_manager),
                    "winner": GameService._get_winner(game_manager) if GameService._is_game_over(game_manager) else None
                }
                return state
            except Exception as e:
                logger.error(f"Error getting game state: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
                return {
                    "error": f"Error getting game state: {str(e)}",
                    "game_id": game_id
                }
        else:
            return {
                "game_id": game_id,
                "trump_card": str(game_manager.trump_card),
                "board": [str(card) for card in game_manager.board_manager.get_board_state()],
                "deckSize": len(game_manager.deck),
                "isGameOver": GameService._is_game_over(game_manager),
                "winner": GameService._get_winner(game_manager) if GameService._is_game_over(game_manager) else None
            }
    
    @staticmethod
    def play_card(game_id, user_id, card_index):
        game_id_str = str(game_id)
        if game_id_str not in ACTIVE_GAMES:
            return {"error": f"Game {game_id} not found or not active"}
        
        game_data = ACTIVE_GAMES[game_id_str]
        game_manager = game_data['manager']
        player = game_data['players'].get(str(user_id))
        
        if not player:
            return {"error": f"Player {user_id} is not part of game {game_id}"}
        
        if GameService._is_game_over(game_manager):
            return {"error": "Game is already over"}
        
        if card_index < 0 or card_index >= len(player.hand):
            return {"error": f"Invalid card index: {card_index}"}
        
        card = player.hand[card_index]
        is_attacker = (game_manager.attacker == player and game_manager.turn_manager.is_attacker_turn)
        is_defender = (game_manager.defender == player and game_manager.turn_manager.is_defender_turn)
        
        if not (is_attacker or is_defender):
            return {"error": "It's not your turn"}
        
        try:
            if is_attacker:
                success = game_manager.turn_manager.execute_attack(card)
                if not success:
                    return {"error": "Invalid attack move"}
            else:
                board_state = game_manager.board_manager.get_board_state()
                if not board_state:
                    return {"error": "No card to defend against"}
                attack_card = board_state[-1]
                success = game_manager.turn_manager.handle_defense(attack_card, card)
                if not success:
                    return {"error": "Invalid defense move"}
            
            if GameService._is_game_over(game_manager):
                GameService._handle_game_over(game_id, game_manager)
                return GameService.get_game_state(game_id, user_id)
            
            GameService._handle_ai_turn(game_id)
            
            if GameService._is_game_over(game_manager):
                GameService._handle_game_over(game_id, game_manager)
            
            return GameService.get_game_state(game_id, user_id)
        except Exception as e:
            logger.error(f"Error playing card: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"error": f"Error playing card: {str(e)}"}
    
    @staticmethod
    def skip_turn(game_id, user_id):
        game_id_str = str(game_id)
        if game_id_str not in ACTIVE_GAMES:
            return {"error": f"Game {game_id} not found or not active"}
        
        game_data = ACTIVE_GAMES[game_id_str]
        game_manager = game_data['manager']
        player = game_data['players'].get(str(user_id))
        
        if not player:
            return {"error": f"Player {user_id} is not part of game {game_id}"}
        
        if GameService._is_game_over(game_manager):
            return {"error": "Game is already over"}
        
        if player != game_manager.attacker or not game_manager.turn_manager.is_attacker_turn:
            return {"error": "Only the attacker can skip their turn"}
        
        try:
            game_manager.round_manager.finalize_round(switch_roles=True)
            game_manager.board_manager.next_round()
            
            GameService._handle_ai_turn(game_id)
            
            if GameService._is_game_over(game_manager):
                GameService._handle_game_over(game_id, game_manager)
            
            return GameService.get_game_state(game_id, user_id)
        except Exception as e:
            logger.error(f"Error skipping turn: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"error": f"Error skipping turn: {str(e)}"}
    
    @staticmethod
    def take_cards(game_id, user_id):
        game_id_str = str(game_id)
        if game_id_str not in ACTIVE_GAMES:
            return {"error": f"Game {game_id} not found or not active"}
        
        game_data = ACTIVE_GAMES[game_id_str]
        game_manager = game_data['manager']
        player = game_data['players'].get(str(user_id))
        
        if not player:
            return {"error": f"Player {user_id} is not part of game {game_id}"}
        
        if GameService._is_game_over(game_manager):
            return {"error": "Game is already over"}
        
        if player != game_manager.defender or not game_manager.turn_manager.is_defender_turn:
            return {"error": "Only the defender can take cards"}
        
        try:
            board_cards = game_manager.board_manager.get_board_state()
            for card in board_cards:
                player.add_card_to_hand(card)
            
            game_manager.round_manager.finalize_round(switch_roles=False)
            game_manager.board_manager.clear_board()
            game_manager.board_manager.next_round()
            
            GameService._handle_ai_turn(game_id)
            
            if GameService._is_game_over(game_manager):
                GameService._handle_game_over(game_id, game_manager)
            
            return GameService.get_game_state(game_id, user_id)
        except Exception as e:
            logger.error(f"Error taking cards: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"error": f"Error taking cards: {str(e)}"}
    
    @staticmethod
    def _handle_ai_turn(game_id):
        game_id_str = str(game_id)
        game_data = ACTIVE_GAMES[game_id_str]
        game_manager = game_data['manager']
        ai_player = game_data['players'].get('AI')
        
        if not ai_player:
            logger.info("No AI player found in this game")
            return
        
        is_ai_attacker = (game_manager.attacker == ai_player and game_manager.turn_manager.is_attacker_turn)
        is_ai_defender = (game_manager.defender == ai_player and game_manager.turn_manager.is_defender_turn)
        
        if not (is_ai_attacker or is_ai_defender):
            logger.info("Not AI's turn")
            return
        
        logger.info(f"AI is {'attacking' if is_ai_attacker else 'defending'}")
        
        if is_ai_attacker:
            logger.info("AI is attacking...")
            ai_attacked = False
            
            for card in sorted(ai_player.hand, key=lambda c: c.weight):
                if game_manager.turn_manager.execute_attack(card):
                    ai_attacked = True
                    logger.info(f"AI attacks with {card}")
                    break
            
            if not ai_attacked:
                logger.info("AI passes its attack")
                game_manager.round_manager.finalize_round(switch_roles=True)
                game_manager.board_manager.next_round()
                
        elif is_ai_defender:
            logger.info("AI is defending...")
            board_state = game_manager.board_manager.get_board_state()
            
            if board_state:
                attack_card = board_state[-1]
                ai_defended = False
                valid_defenses = []
                
                for card in ai_player.hand:
                    if card.suit == attack_card.suit and card.weight > attack_card.weight:
                        valid_defenses.append(card)
                    elif card.is_trump(game_manager.trump_card.suit) and not attack_card.is_trump(game_manager.trump_card.suit):
                        valid_defenses.append(card)
                
                if valid_defenses:
                    defense_card = min(valid_defenses, key=lambda c: c.weight)
                    if game_manager.turn_manager.handle_defense(attack_card, defense_card):
                        ai_defended = True
                        logger.info(f"AI defends with {defense_card}")
                
                if not ai_defended:
                    logger.info("AI takes all cards")
                    for board_card in board_state:
                        ai_player.add_card_to_hand(board_card)
                    game_manager.round_manager.finalize_round(switch_roles=False)
                    game_manager.board_manager.clear_board()
                    game_manager.board_manager.next_round()
    
    @staticmethod
    def _is_game_over(game_manager):
        deck_empty = len(game_manager.deck) == 0
        player1_has_no_cards = len(game_manager.players[0].hand) == 0
        player2_has_no_cards = len(game_manager.players[1].hand) == 0
        return deck_empty and (player1_has_no_cards or player2_has_no_cards)
    
    @staticmethod
    def _get_winner(game_manager):
        if not GameService._is_game_over(game_manager):
            return None
        
        player1_has_no_cards = len(game_manager.players[0].hand) == 0
        player2_has_no_cards = len(game_manager.players[1].hand) == 0
        
        if player1_has_no_cards and player2_has_no_cards:
            return "draw"
        if player1_has_no_cards:
            return game_manager.players[0].name
        if player2_has_no_cards:
            return game_manager.players[1].name
        
        return "draw"
    
    @staticmethod
    def _handle_game_over(game_id, game_manager):
        winner_name = GameService._get_winner(game_manager)
        
        try:
            game_id_int = int(game_id)
            game_session = GameSession.query.get(game_id_int)
        except (ValueError, TypeError):
            logger.error(f"Could not convert game_id {game_id} to integer")
            game_session = None
        
        if not game_session:
            logger.error(f"Game session {game_id} not found in database")
            return
        
        game_session.end_time = datetime.utcnow()
        game_session.game_state = "completed"
        
        if winner_name == "draw":
            game_session.winner = "draw"
        else:
            game_id_str = str(game_id)
            for player_id, player in ACTIVE_GAMES[game_id_str]['players'].items():
                if player.name == winner_name:
                    game_session.winner = player_id
                    break
        
        if game_session.is_against_ai:
            human_player_id = game_session.players.split(',')[0]
            user = User.query.get(human_player_id)
            
            if user:
                if winner_name == "draw":
                    user.number_of_draws = (user.number_of_draws or 0) + 1
                elif game_session.winner == human_player_id:
                    user.number_of_wins = (user.number_of_wins or 0) + 1
                else:
                    user.number_of_losses = (user.number_of_losses or 0) + 1
        
        try:
            db.session.commit()
            logger.info(f"Game session updated: winner={game_session.winner}, state={game_session.game_state}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating game session: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())