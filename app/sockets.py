from flask_socketio import SocketIO, emit
from app import socketio

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('move')
def handle_move(data):
    print('Move received:', data)
    emit('update', {'data': 'Move processed'}, broadcast=True)
