# File path: app/game/events.py

# Add these imports if not already at the top
import json
from app.extensions import socketio
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from flask import session, request
from app.services.game_service import GameService
import logging

logger = logging.getLogger(__name__)

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        logger.info(f"Client connected: User {current_user.id}")
        emit('connection_response', {'status': 'connected', 'user_id': current_user.id})
    else:
        logger.warning(f"Unauthenticated client connection attempt")
        emit('connection_response', {'status': 'error', 'message': 'Authentication required'})

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        logger.info(f"Client disconnected: User {current_user.id}")
    else:
        logger.info("Unauthenticated client disconnected")

@socketio.on('join_game')
def handle_join_game(data):
    game_id = data.get('game_id')
    if not game_id:
        logger.warning(f"Join game attempt without game_id: User {current_user.id}")
        emit('error', {'message': 'Game ID is required'})
        return
        
    logger.info(f"User {current_user.id} joining game {game_id}")
    join_room(game_id)
    emit('player_joined', {
        'user_id': current_user.id,
        'username': current_user.username
    }, room=game_id, include_self=False)
    
    try:
        game_state = GameService.get_game_state(game_id, current_user.id)
        emit('game_state', game_state)
        
        # If game is in progress and it's not the player's turn, check if AI should move
        if game_state.get('board', []):
            logger.info(f"Game {game_id} already in progress, sending update")
            emit('game_updated', game_state)
        elif (game_id in ACTIVE_GAMES and
              'AI' in ACTIVE_GAMES[game_id]['players'] and
              game_state.get('attackerName', '').startswith('AI_') and
              not game_state.get('isPlayerTurn', False)):
            logger.info(f"AI's turn to start game {game_id}, scheduling AI move")
            # Call AI turn handler directly with a shorter delay
            from threading import Timer
            Timer(0.3, lambda: GameService._handle_ai_turn(game_id)).start()
    except ValueError as e:
        logger.error(f"Error getting game state: {str(e)}")
        emit('error', {'message': str(e)})

@socketio.on('leave_game')
def handle_leave_game(data):
    game_id = data.get('game_id')
    if not game_id:
        logger.warning(f"Leave game attempt without game_id: User {current_user.id}")
        return
    logger.info(f"User {current_user.id} leaving game {game_id}")
    leave_room(game_id)
    emit('player_left', {
        'user_id': current_user.id,
        'username': current_user.username
    }, room=game_id)

@socketio.on('play_card')
def handle_play_card(data):
    game_id = data.get('game_id')
    card_index = data.get('card_index')
    
    if not game_id or card_index is None:
        logger.warning(f"Play card attempt with invalid data: User {current_user.id}, Data: {data}")
        emit('error', {'message': 'Game ID and card index are required'})
        return
        
    logger.info(f"User {current_user.id} playing card at index {card_index} in game {game_id}")
    
    try:
        result = GameService.play_card(game_id, current_user.id, card_index)
        
        if 'error' in result:
            logger.warning(f"Error playing card: {result['error']}")
            emit('error', {'message': result['error']})
        else:
            # Broadcast the updated game state to all players in the room
            emit('game_updated', result, room=game_id)
            
            # Check if the game is over
            if result.get('isGameOver'):
                logger.info(f"Game {game_id} over, winner: {result.get('winner')}")
                emit('game_over', {
                    'winner': result.get('winner'),
                    'game_id': game_id
                }, room=game_id)
                
            # If it's AI's turn after this move, schedule AI move with shorter delay
            elif (game_id in ACTIVE_GAMES and 
                  'AI' in ACTIVE_GAMES[game_id]['players'] and
                  ((result.get('attackerName', '').startswith('AI_') and result.get('isPlayerTurn') == False) or
                   (result.get('defenderName', '').startswith('AI_') and result.get('isPlayerTurn') == False))):
                from threading import Timer
                Timer(0.3, lambda: GameService._handle_ai_turn(game_id)).start()
    except ValueError as e:
        logger.error(f"Error playing card: {str(e)}")
        emit('error', {'message': str(e)})

@socketio.on('request_game_state')
def handle_request_game_state(data):
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
            # Broadcast to all players
            emit('game_updated', result, room=game_id)
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
            # Broadcast to all players
            emit('game_updated', result, room=game_id)
            if result.get('isGameOver'):
                logger.info(f"Game {game_id} over, winner: {result.get('winner')}")
                emit('game_over', {
                    'winner': result.get('winner'),
                    'game_id': game_id
                }, room=game_id)
    except ValueError as e:
        logger.error(f"Error taking cards: {str(e)}")
        emit('error', {'message': str(e)})