from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from flask import session, request
from app import socketio
from app.services.game_service import GameService

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    if current_user.is_authenticated:
        emit('connection_response', {'status': 'connected', 'user_id': current_user.id})
    else:
        emit('connection_response', {'status': 'error', 'message': 'Authentication required'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')
    # You might want to handle game cleanup here for the disconnecting user

@socketio.on('join_game')
def handle_join_game(data):
    """Join a specific game room"""
    game_id = data.get('game_id')
    if not game_id:
        emit('error', {'message': 'Game ID is required'})
        return
    
    # Join the game's room
    join_room(game_id)
    
    # Notify others
    emit('player_joined', {
        'user_id': current_user.id,
        'username': current_user.username
    }, room=game_id, include_self=False)
    
    # Get and send game state to the joining player
    try:
        game_state = GameService.get_game_state(game_id, current_user.id)
        emit('game_state', game_state)
    except ValueError as e:
        emit('error', {'message': str(e)})

@socketio.on('leave_game')
def handle_leave_game(data):
    """Leave a game room"""
    game_id = data.get('game_id')
    if not game_id:
        return
    
    leave_room(game_id)
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
        emit('error', {'message': 'Game ID and card index are required'})
        return
    
    try:
        # Play the card
        result = GameService.play_card(game_id, current_user.id, card_index)
        
        # Broadcast updated game state to all players in the room
        emit('game_updated', result, room=game_id)
    except ValueError as e:
        emit('error', {'message': str(e)})

@socketio.on('request_game_state')
def handle_request_game_state(data):
    """Handle a request for the current game state"""
    game_id = data.get('game_id')
    
    if not game_id:
        emit('error', {'message': 'Game ID is required'})
        return
    
    try:
        game_state = GameService.get_game_state(game_id, current_user.id)
        emit('game_state', game_state)
    except ValueError as e:
        emit('error', {'message': str(e)})

@socketio.on('skip_turn')
def handle_skip_turn(data):
    """Handle a player skipping their turn"""
    game_id = data.get('game_id')
    
    if not game_id:
        emit('error', {'message': 'Game ID is required'})
        return
    
    try:
        # TODO: Implement skip turn logic in GameService
        # result = GameService.skip_turn(game_id, current_user.id)
        
        # Placeholder
        result = {'status': 'success', 'message': 'Turn skipped'}
        
        # Broadcast updated game state to all players in the room
        emit('game_updated', result, room=game_id)
    except ValueError as e:
        emit('error', {'message': str(e)})

@socketio.on('take_cards')
def handle_take_cards(data):
    """Handle a player taking cards"""
    game_id = data.get('game_id')
    
    if not game_id:
        emit('error', {'message': 'Game ID is required'})
        return
    
    try:
        # TODO: Implement take cards logic in GameService
        # result = GameService.take_cards(game_id, current_user.id)
        
        # Placeholder
        result = {'status': 'success', 'message': 'Cards taken'}
        
        # Broadcast updated game state to all players in the room
        emit('game_updated', result, room=game_id)
    except ValueError as e:
        emit('error', {'message': str(e)})