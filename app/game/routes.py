# File path: app/game/routes.py

from flask import render_template, redirect, url_for, jsonify, session, flash, request
from flask_login import login_required, current_user
from app.game import bp
from app.models import GameSession, User
from app.services.game_service import GameService
import logging

logger = logging.getLogger(__name__)

@bp.route("/")
@login_required
def index():
    return render_template('game/index.html', title='Play Durak')

@bp.route("/play")
@login_required
def play():
    # Get game ID from query parameters or session
    game_id = request.args.get('game_id') or session.get('game_id')
    logger.info(f"Playing game with id: {game_id}, from args: {request.args.get('game_id')}, from session: {session.get('game_id')}")
    
    if not game_id:
        flash('No active game found. Please start a new game.', 'warning')
        return redirect(url_for('game.index'))
    
    try:
        # Check if game exists in database
        game_session = GameSession.query.get(game_id)
        logger.info(f"Game session query result: {game_session}")
        
        if not game_session:
            flash('The requested game does not exist.', 'warning')
            return redirect(url_for('game.index'))
        
        # Check if user is part of this game
        players = game_session.players.split(',')
        logger.info(f"Game players: {players}, current user: {current_user.id}")
        
        if str(current_user.id) not in players and not game_session.is_against_ai:
            flash('You are not part of this game.', 'warning')
            return redirect(url_for('game.index'))
        
    except Exception as e:
        logger.error(f"ERROR checking game: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        flash(f'Error loading game: {str(e)}', 'danger')
        return redirect(url_for('game.index'))
    
    # Store game ID in session
    session['game_id'] = game_id
    
    return render_template('game/game.html', title='Durak Game', game_id=game_id)

@bp.route("/play_with_ai")
@login_required
def play_with_ai():
    try:
        logger.info(f"Creating AI game for user {current_user.id}")
        
        # Create a new game against AI
        game_data = GameService.create_ai_game(current_user.id)
        logger.info(f"Game created: {game_data}")
        
        game_id = game_data['game_id']
        session['game_id'] = game_id
        logger.info(f"Stored game_id in session: {game_id}")
        
        # Redirect to the game page
        return redirect(url_for('game.play', game_id=game_id))
        
    except Exception as e:
        logger.error(f"ERROR creating game: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        flash(f'Error creating game: {str(e)}', 'danger')
        return redirect(url_for('game.index'))

@bp.route("/play_with_friend")
@login_required
def play_with_friend():
    flash('Play with friend feature is not implemented yet.', 'info')
    return redirect(url_for('game.index'))

@bp.route("/random_match")
@login_required
def random_match():
    flash('Random match feature is not implemented yet.', 'info')
    return redirect(url_for('game.index'))

@bp.route("/state")
@login_required
def game_state():
    game_id = request.args.get('game_id') or session.get('game_id')
    
    if not game_id:
        return jsonify({"error": "No active game"}), 404
    
    try:
        game_state = GameService.get_game_state(game_id, current_user.id)
        return jsonify(game_state)
    except Exception as e:
        logger.error(f"Error getting game state: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/history")
@login_required
def game_history():
    games = GameSession.query.filter(
        GameSession.players.like(f'%{current_user.id}%')
    ).order_by(GameSession.start_time.desc()).all()
    
    return render_template('game/history.html', title='Game History', games=games)

@bp.route("/rules")
def rules():
    return render_template('rules.html', title='Durak Rules')
