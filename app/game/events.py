from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from flask import session, request
from app import socketio
from app.services.game_service import GameService
import logging

# Setup logging
logger = logging.getLogger(__name__)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    if current_user.is_authenticated:
        logger.info(f"Client connected: User {current_user.id}")
        emit('connection_response', {'status': 'connected', 'user_id': current_user.id})
    else:
        logger.warning(f"Unauthenticated client connection attempt")
        emit('connection_response', {'status': 'error', 'message': 'Authentication required'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    if current_user.is_authenticated:
        logger.info(f"Client disconnected: User {current_user.id}")
    else:
        logger.info("Unauthenticated client disconnected")

@socketio.on('join_game')
def handle_join_game(data):
    """Handle a player joining a game"""
    game_id = data.get('game_id')
    if not game_id:
        logger.warning(f"Join game attempt without game_id: User {current_user.id}")
        emit('error', {'message': 'Game ID is required'})
        return
    
    logger.info(f"User {current_user.id} joining game {game_id}")
    join_room(game_id)
    
    # Notify other players in the room
    emit('player_joined', {
        'user_id': current_user.id,
        'username': current_user.username
    }, room=game_id, include_self=False)
    
    try:
        # Get game state for this player
        game_state = GameService.get_game_state(game_id, current_user.id)
        emit('game_state', game_state)
    except ValueError as e:
        logger.error(f"Error getting game state: {str(e)}")
        emit('error', {'message': str(e)})

@socketio.on('leave_game')
def handle_leave_game(data):
    """Handle a player leaving a game"""
    game_id = data.get('game_id')
    if not game_id:
        logger.warning(f"Leave game attempt without game_id: User {current_user.id}")
        return
    
    logger.info(f"User {current_user.id} leaving game {game_id}")
    leave_room(game_id)
    
    # Notify other players in the room
    emit('player_left', {
        'user_id': current_user.id,
        'username': current_user.username
    }, room=game_id)

@socketio.on('play_card')
def handle_play_card(data):
    """Handle a player playing a card"""
    game_id = data.get('game_id')
    card_index = data.get('card_index')
    
    if not game_id or card_index is None:
        logger.warning(f"Play card attempt with invalid data: User {current_user.id}, Data: {data}")
        emit('error', {'message': 'Game ID and card index are required'})
        return
    
    logger.info(f"User {current_user.id} playing card at index {card_index} in game {game_id}")
    try:
        # Process the move through GameService
        result = GameService.play_card(game_id, current_user.id, card_index)
        
        if 'error' in result:
            logger.warning(f"Error playing card: {result['error']}")
            emit('error', {'message': result['error']})
        else:
            # Broadcast updated game state to all players in the room
            emit('game_updated', result, room=game_id)
            
            # If the game is over, send game_over event
            if result.get('isGameOver'):
                logger.info(f"Game {game_id} over, winner: {result.get('winner')}")
                emit('game_over', {
                    'winner': result.get('winner'),
                    'game_id': game_id
                }, room=game_id)
    except ValueError as e:
        logger.error(f"Error playing card: {str(e)}")
        emit('error', {'message': str(e)})

@socketio.on('request_game_state')
def handle_request_game_state(data):
    """Handle a request for current game state"""
    game_id = data.get('game_id')
    if not game_id:
        logger.warning(f"Game state request without game_id: User {current_user.id}")
        emit('error', {'message': 'Game ID is required'})
        return
    
    logger.info(f"User {current_user.id} requesting game state for game {game_id}")
    try:
        game_state = GameService.get_game_state(game_id, current_user.id)
        emit('game_state', game_state)
    except ValueError as e:
        logger.error(f"Error getting game state: {str(e)}")
        emit('error', {'message': str(e)})

@socketio.on('skip_turn')
def handle_skip_turn(data):
    """Handle a player skipping their turn"""
    game_id = data.get('game_id')
    if not game_id:
        logger.warning(f"Skip turn attempt without game_id: User {current_user.id}")
        emit('error', {'message': 'Game ID is required'})
        return
    
    logger.info(f"User {current_user.id} skipping turn in game {game_id}")
    try:
        result = GameService.skip_turn(game_id, current_user.id)
        
        if 'error' in result:
            logger.warning(f"Error skipping turn: {result['error']}")
            emit('error', {'message': result['error']})
        else:
            # Broadcast updated game state to all players in the room
            emit('game_updated', result, room=game_id)
            
            # If the game is over, send game_over event
            if result.get('isGameOver'):
                logger.info(f"Game {game_id} over, winner: {result.get('winner')}")
                emit('game_over', {
                    'winner': result.get('winner'),
                    'game_id': game_id
                }, room=game_id)
    except ValueError as e:
        logger.error(f"Error skipping turn: {str(e)}")
        emit('error', {'message': str(e)})

@socketio.on('take_cards')
def handle_take_cards(data):
    """Handle a player taking all cards from the board"""
    game_id = data.get('game_id')
    if not game_id:
        logger.warning(f"Take cards attempt without game_id: User {current_user.id}")
        emit('error', {'message': 'Game ID is required'})
        return
    
    logger.info(f"User {current_user.id} taking cards in game {game_id}")
    try:
        result = GameService.take_cards(game_id, current_user.id)
        
        if 'error' in result:
            logger.warning(f"Error taking cards: {result['error']}")
            emit('error', {'message': result['error']})
        else:
            # Broadcast updated game state to all players in the room
            emit('game_updated', result, room=game_id)
            
            # If the game is over, send game_over event
            if result.get('isGameOver'):
                logger.info(f"Game {game_id} over, winner: {result.get('winner')}")
                emit('game_over', {
                    'winner': result.get('winner'),
                    'game_id': game_id
                }, room=game_id)
    except ValueError as e:
        logger.error(f"Error taking cards: {str(e)}")
        emit('error', {'message': str(e)})

@socketio.on('start_game')
def handle_start_game(data):
    """Handle a request to start a new game"""
    against_ai = data.get('against_ai', True)
    
    logger.info(f"User {current_user.id} starting new game against AI: {against_ai}")
    try:
        # Create a new game
        game_data = GameService.create_ai_game(current_user.id) if against_ai else None
        
        if not game_data:
            logger.error("Failed to create game")
            emit('error', {'message': 'Failed to create game'})
            return
            
        game_id = game_data['game_id']
        
        # Join the game room
        join_room(game_id)
        
        # Save game_id to session
        session['game_id'] = game_id
        
        # Send game created event
        emit('game_created', game_data)
        
        # Send initial game state
        game_state = GameService.get_game_state(game_id, current_user.id)
        emit('game_state', game_state)
        
    except Exception as e:
        logger.error(f"Error starting game: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        emit('error', {'message': f'Error starting game: {str(e)}'})