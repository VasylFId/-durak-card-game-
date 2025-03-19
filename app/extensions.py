# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()

# Configure login manager
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'