from flask import render_template, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from app.game import bp
from app.models import GameSession
from app.services.game_service import GameService

@bp.route("/")
@login_required
def index():
    return render_template('game/index.html', title='Play Durak')

@bp.route("/play")
@login_required
def play():
    return render_template('game/game.html', title='Game')

@bp.route("/play_with_ai")
@login_required
def play_with_ai():
    # Create a new game against AI
    game_data = GameService.create_ai_game(current_user.id)
    session['game_id'] = game_data['game_id']
    return redirect(url_for('game.play'))

@bp.route("/play_with_friend")
@login_required
def play_with_friend():
    # Logic to set up a game with a friend (placeholder)
    return redirect(url_for('game.play'))

@bp.route("/random_match")
@login_required
def random_match():
    # Logic to start a random match with another player (placeholder)
    return redirect(url_for('game.play'))

@bp.route("/state")
@login_required
def game_state():
    game_id = session.get('game_id')
    if not game_id:
        return jsonify({"error": "No active game"}), 404
    
    # Get current game state
    game_state = GameService.get_game_state(game_id, current_user.id)
    return jsonify(game_state)