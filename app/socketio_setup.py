from flask_socketio import SocketIO
from app.services.game_service_integration import connect_game_socket_events

# Create a single SocketIO instance that can be imported and used throughout the application
socketio = SocketIO()

def init_socketio(app):
    """Initialize SocketIO with the Flask app and connect event handlers"""
    # Initialize with broader CORS settings to prevent connection issues
    socketio.init_app(app, 
                     cors_allowed_origins="*", 
                     async_mode='threading',
                     logger=True, 
                     engineio_logger=True)
    
    # Connect all game socket events
    connect_game_socket_events(socketio)
    
    return socketio