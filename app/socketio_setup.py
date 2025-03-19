# app/socketio_setup.py

from flask_socketio import SocketIO
from app.services.game_service_integration import connect_game_socket_events

# Initialize SocketIO instance
socketio = SocketIO()

def init_socketio(app):
    """Initialize SocketIO with the Flask app and connect event handlers"""
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Connect all Socket.IO event handlers
    connect_game_socket_events(socketio)
    
    return socketio