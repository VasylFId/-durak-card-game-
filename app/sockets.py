from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request
from app.services.game_service import GameService

socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_game')
def handle_join_game(data):
    game_id = data['game_id']
    user_id = data['user_id']
    
    # Join the game's room
    join_room(game_id)
    
    # Notify others
    emit('player_joined', {'user_id': user_id}, room=game_id, include_self=False)
    
    # Send game state to the joining player
    game_state = GameService.get_game_state(game_id)
    emit('game_state', game_state)

@socketio.on('play_card')
def handle_play_card(data):
    game_id = data['game_id']
    user_id = data['user_id']
    card_index = data['card_index']
    
    # Process the move in game logic
    result = GameService.play_card(game_id, user_id, card_index)
    
    # Broadcast updated game state to all players in the room
    emit('game_updated', result, room=game_id)

@socketio.on('start_game')
def handle_start_game(data):
    user_id = data['user_id']
    against_ai = data.get('against_ai', True)
    
    # Create new game
    game_data = GameService.create_game(user_id, against_ai)
    game_id = game_data['game_id']
    
    # Join the game room
    join_room(game_id)
    
    # Return game data to client
    emit('game_created', game_data)