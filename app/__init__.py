# app/__init__.py

from flask import Flask, render_template
from config import Config
from app.extensions import db, bcrypt, login_manager, socketio


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register blueprints
    from app.auth.routes import bp as auth_bp
    from app.main.routes import bp as main_bp
    from app.game.routes import bp as game_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(game_bp)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    # Setup socket event handlers
    from app.services.game_service_integration import connect_game_socket_events
    connect_game_socket_events(socketio)
    
    return app