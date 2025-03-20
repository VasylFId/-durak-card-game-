# File path: app/services/game_service.py

from app.extensions import socketio
import uuid
import json
from datetime import datetime
from flask_login import current_user
from app.extensions import db
from app.models import GameSession, User
from game_logic.card_package import Deck, Card, Suit, Rank
from game_logic.players.player import Player
from game_logic.game_management.game import DurakGameManager
from game_logic.game_management.round_manager import RoundManager
import logging

logger = logging.getLogger(__name__)

# This should be a global variable outside of any functions
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
            
            # Ensure turn manager is properly initialized
            if hasattr(game_manager, 'turn_manager') and game_manager.turn_manager:
                # Make sure turn manager knows who is attacker and defender
                game_manager.turn_manager.set_players(game_manager.attacker, game_manager.defender)
                
                # Ensure turn state is correct (attacker's turn)
                game_manager.turn_manager.is_attacker_turn = True
                game_manager.turn_manager.is_defender_turn = False
                logger.info(f"Turn state initialized: attacker ({game_manager.attacker.name}) turn")
            
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
                    
                # Get discard pile info (if available)
                discard_pile = []
                if hasattr(game_manager.board_manager, 'get_discard_pile'):
                    discard_pile = [str(card) for card in game_manager.board_manager.get_discard_pile()]
                else:
                    # Fallback if the method doesn't exist
                    discard_pile = []
                
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
                    "winner": GameService._get_winner(game_manager) if GameService._is_game_over(game_manager) else None,
                    "discardPile": discard_pile,
                    "roundNumber": game_manager.round_manager.round_number if hasattr(game_manager, 'round_manager') else 0
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
            logger.info("Player is skipping turn - ending attack phase")
            
            # Store original roles for logging
            original_attacker = game_manager.attacker
            original_defender = game_manager.defender
            
            # Move cards to discard pile
            game_manager.board_manager.move_to_discard_pile()
            
            # Finalize round with roles switching
            roles_switched = game_manager.round_manager.finalize_round(roles_should_switch=True)
            logger.info(f"Round finalized, roles will switch: {roles_switched}")

            logger.info(f"Roles before round change - Original attacker: {original_attacker.name}, Original defender: {original_defender.name}")

            # Initialize new round
            game_manager.attacker, game_manager.defender = game_manager.round_manager.initialize_round(
                game_manager.attacker,
                game_manager.defender,
                game_manager.deck
            )
            
            # Update turn manager with new roles
            if hasattr(game_manager, 'turn_manager') and game_manager.turn_manager:
                game_manager.turn_manager.set_players(game_manager.attacker, game_manager.defender)
                game_manager.turn_manager.reset_turn_state()
            
            logger.info(f"Roles after round change - New attacker: {game_manager.attacker.name}, New defender: {game_manager.defender.name}")
            
            # Deal new cards
            GameService._deal_new_cards(game_manager)
            
            # If AI is now the attacker, trigger its move after a short delay
            if game_manager.attacker.name.startswith('AI_') and game_manager.turn_manager.is_attacker_turn:
                from threading import Timer
                Timer(0.5, lambda: GameService._handle_ai_turn(game_id)).start()
            
            # Check for game over
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
            logger.info(f"Player {player.name} is taking cards from the board")
            board_cards = game_manager.board_manager.get_board_state()
            logger.info(f"Cards being taken: {board_cards}")
            
            # Add all cards from board to player's hand
            for card in board_cards:
                player.add_card_to_hand(card)
            
            # Finalize round WITHOUT switching roles
            game_manager.round_manager.finalize_round(roles_should_switch=False)
            game_manager.board_manager.clear_board()
            game_manager.board_manager.next_round()
            
            # Deal new cards to both players
            GameService._deal_new_cards(game_manager)
            
            # Reset turn manager state to make it attacker's turn again
            if hasattr(game_manager, 'turn_manager') and game_manager.turn_manager:
                game_manager.turn_manager.reset_turn_state()
                game_manager.turn_manager.is_attacker_turn = True
                game_manager.turn_manager.is_defender_turn = False
            
            logger.info(f"After taking cards - Attacker: {game_manager.attacker.name}, Defender: {game_manager.defender.name}")
            logger.info(f"Attacker's turn: {game_manager.turn_manager.is_attacker_turn}, Defender's turn: {game_manager.turn_manager.is_defender_turn}")
            
            # If it's AI's turn after player took cards, trigger AI move
            if (game_manager.attacker.name.startswith('AI_') and 
                game_manager.turn_manager.is_attacker_turn):
                logger.info("AI's turn after player took cards - triggering AI move")
                # Add a slight delay for better user experience
                from threading import Timer
                Timer(0.5, lambda: GameService._handle_ai_turn(game_id)).start()
            
            # Check for game over condition
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
        logger.info(f"AI turn handler called for game {game_id}")
        game_id_str = str(game_id)
        if game_id_str not in ACTIVE_GAMES:
            logger.error(f"Game {game_id} not found in active games")
            return
        
        game_data = ACTIVE_GAMES[game_id_str]
        game_manager = game_data['manager']
        
        logger.info(f"Explicit Turn States: attacker_turn={game_manager.turn_manager.is_attacker_turn}, defender_turn={game_manager.turn_manager.is_defender_turn}")
        
        ai_player = game_data['players'].get('AI')
        if not ai_player:
            logger.info("No AI player found in this game")
            return
        
        logger.info(f"AI hand: {ai_player.hand}")
        logger.info(f"Current attacker: {game_manager.attacker.name}")
        logger.info(f"Current defender: {game_manager.defender.name}")
        logger.info(f"Is attacker's turn: {game_manager.turn_manager.is_attacker_turn}")
        logger.info(f"Is defender's turn: {game_manager.turn_manager.is_defender_turn}")
        
        is_ai_attacker = (game_manager.attacker == ai_player and game_manager.turn_manager.is_attacker_turn)
        is_ai_defender = (game_manager.defender == ai_player and game_manager.turn_manager.is_defender_turn)
        
        if not (is_ai_attacker or is_ai_defender):
            logger.info("Not AI's turn - exiting AI turn handler")
            return
        
        logger.info(f"AI is {'attacking' if is_ai_attacker else 'defending'}")
        
        from game_logic.game_management.user_input_manager import UserInputManager
        user_input_manager = UserInputManager()
        
        if is_ai_attacker:
            logger.info("AI is attacking...")
            ai_attacked = False
            
            suggested_card = user_input_manager._UserInputManager__get_suggested_card_to_attack(
                game_manager.board_manager,
                ai_player
            )
            
            if suggested_card:
                logger.info(f"UserInputManager suggested card for attack: {suggested_card}")
                if game_manager.turn_manager.execute_attack(suggested_card):
                    ai_attacked = True
                    logger.info(f"AI successfully attacked with {suggested_card}")
                    updated_state = GameService.get_game_state(game_id)
                    socketio.emit('game_updated', updated_state, room=game_id_str)
            else:
                logger.info("No card suggested for attack, AI skipping turn")
            
            if not ai_attacked:
                logger.info("AI could not attack, passing turn")
                # Clear board and move cards to discard
                game_manager.board_manager.move_to_discard_pile()
                game_manager.round_manager.finalize_round(roles_should_switch=True)
                game_manager.board_manager.next_round()
                
                # Switch roles and reset turn state
                game_manager.attacker, game_manager.defender = game_manager.defender, game_manager.attacker
                if hasattr(game_manager, 'turn_manager') and game_manager.turn_manager:
                    game_manager.turn_manager.set_players(game_manager.attacker, game_manager.defender)
                    game_manager.turn_manager.reset_turn_state()
                
                # Deal new cards before emitting updated state
                GameService._deal_new_cards(game_manager)
                updated_state = GameService.get_game_state(game_id)
                socketio.emit('game_updated', updated_state, room=game_id_str)
        
        elif is_ai_defender:
            logger.info("AI is defending...")
            board_state = game_manager.board_manager.get_board_state()
            
            if board_state:
                attack_card = board_state[-1]
                ai_defended = False
                
                suggested_card = user_input_manager._UserInputManager__get_suggested_card_to_defend(
                    game_manager.board_manager,
                    ai_player,
                    attack_card
                )
                
                if suggested_card:
                    logger.info(f"UserInputManager suggested card for defense: {suggested_card}")
                    if game_manager.turn_manager.handle_defense(attack_card, suggested_card):
                        ai_defended = True
                        logger.info(f"AI successfully defended with {suggested_card}")
                        updated_state = GameService.get_game_state(game_id)
                        socketio.emit('game_updated', updated_state, room=game_id_str)
                else:
                    logger.info("No valid defense card suggested, AI taking cards")
                
                # If AI couldn't defend, take all cards on the board
                if not ai_defended:
                    logger.info("AI cannot defend, taking cards")
                    
                    # Add all cards from the board to AI's hand
                    for card in board_state:
                        ai_player.add_card_to_hand(card)
                    
                    # Finalize round with roles_should_switch=False since defender takes cards
                    game_manager.round_manager.finalize_round(roles_should_switch=False)
                    game_manager.board_manager.clear_board()
                    game_manager.board_manager.next_round()
                    
                    # Reset turn manager state for attacker's turn
                    if hasattr(game_manager, 'turn_manager') and game_manager.turn_manager:
                        game_manager.turn_manager.reset_turn_state()
                        game_manager.turn_manager.is_attacker_turn = True
                        game_manager.turn_manager.is_defender_turn = False
                    
                    # Deal new cards before emitting updated state
                    GameService._deal_new_cards(game_manager)
                    updated_state = GameService.get_game_state(game_id)
                    socketio.emit('game_updated', updated_state, room=game_id_str)

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
            
            # Broadcast game over event through SocketIO
            from app.extensions import socketio
            socketio.emit('game_over', {
                'winner': winner_name,
                'game_id': game_id
            }, room=game_id)
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating game session: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

    @staticmethod
    def _deal_new_cards(game_manager):
        """
        Deal new cards to players after a round to maintain hand size (typically 6).
        Also handles the case where the deck is depleted except for the trump card.
        """
        # Check if the deck has only the trump card left
        if len(game_manager.deck) == 0 and game_manager.deck.trump_card is not None:
            logger.info("Deck empty except for trump card - offering trump card")
            trump_card = game_manager.deck.draw_trump_card()
            if trump_card:
                # In Durak rules, the player who needs to draw first gets the trump card
                if len(game_manager.attacker.hand) < 6:
                    receiver = game_manager.attacker
                else:
                    receiver = game_manager.defender
                    
                receiver.add_card_to_hand(trump_card)
                logger.info(f"Trump card {trump_card} given to {receiver.name}")
                return
        
        # Regular card dealing logic
        attacker = game_manager.attacker
        while len(attacker.hand) < 6 and not game_manager.deck.is_empty():
            card = game_manager.deck.draw_card()
            attacker.add_card_to_hand(card)
            logger.info(f"Dealt card {card} to {attacker.name}")

        defender = game_manager.defender
        while len(defender.hand) < 6 and not game_manager.deck.is_empty():
            card = game_manager.deck.draw_card()
            defender.add_card_to_hand(card)
            logger.info(f"Dealt card {card} to {defender.name}")
            
        # Check one more time if the deck is now empty except for trump card
        if len(game_manager.deck) == 0 and game_manager.deck.trump_card is not None:
            logger.info("After dealing, trump card remains - offering to next player needing cards")
            trump_card = game_manager.deck.draw_trump_card()
            if trump_card:
                if len(attacker.hand) < 6:
                    attacker.add_card_to_hand(trump_card)
                    logger.info(f"Remaining trump card {trump_card} given to {attacker.name}")
                elif len(defender.hand) < 6:
                    defender.add_card_to_hand(trump_card)
                    logger.info(f"Remaining trump card {trump_card} given to {defender.name}")