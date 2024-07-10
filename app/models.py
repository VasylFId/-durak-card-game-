from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    number_of_wins = db.Column(db.Integer, default=0)
    number_of_draws = db.Column(db.Integer, default=0)
    number_of_losses = db.Column(db.Integer, default=0)
    total_games = db.Column(db.Integer, default=0)
    games_against_ai = db.Column(db.Integer, default=0)
    games_against_real_players = db.Column(db.Integer, default=0)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.Column(db.String, nullable=False)  # Store player IDs as a string, or create a relationship
    winner = db.Column(db.String, nullable=True)  # ID of the winning player
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    moves = db.Column(db.Text, nullable=True)  # Store moves as a text or JSON string
    game_state = db.Column(db.String, nullable=False, default='ongoing')
    is_against_ai = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"GameSession('{self.id}', '{self.players}', '{self.game_state}')"
