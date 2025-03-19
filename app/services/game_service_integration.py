# File path: app/services/game_service_integration.py

import logging
import json
from flask import session
from flask_socketio import emit, join_room
from flask_login import current_user
from app.services.game_service import GameService, ACTIVE_GAMES
from app.extensions import socketio

logger = logging.getLogger(__name__)

def connect_game_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        if current_user.is_authenticated:
            logger.info(f"Client connected: User {current_user.id}")
            emit('connection_response', {'status': 'connected', 'user_id': current_user.id})
        else:
            logger.warning(f"Unauthenticated client connection attempt")
            emit('connection_response', {'status': 'error', 'message': 'Authentication required'})
            
    @socketio.on('join_game')
    def handle_join_game(data):
        game_id = data.get('game_id')
        if not game_id:
            logger.warning(f"Join game attempt without game_id: User {current_user.id}")
            emit('error', {'message': 'Game ID is required'})
            return
        
        logger.info(f"User {current_user.id} joining game {game_id}")
        join_room(game_id)
        emit('player_joined', {
            'user_id': current_user.id,
            'username': current_user.username
        }, room=game_id, include_self=False)
        
        try:
            # Get the initial game state
            game_state = GameService.get_game_state(game_id, current_user.id)
            emit('game_state', game_state)
            
            # Check if AI should make first move (AI is attacker and board is empty)
            if (game_id in ACTIVE_GAMES and 
                'AI' in ACTIVE_GAMES[game_id]['players'] and 
                not game_state.get('board', [])):
                
                game_manager = ACTIVE_GAMES[game_id]['manager']
                ai_player = ACTIVE_GAMES[game_id]['players'].get('AI')
                
                # If AI is the attacker and it's attacker's turn, make AI move
                if (ai_player and 
                    game_manager.attacker == ai_player and 
                    game_manager.turn_manager.is_attacker_turn):
                    
                    logger.info(f"Triggering initial AI move for game {game_id}")
                    # Give a slight delay to let frontend initialize fully
                    from threading import Timer
                    Timer(1.0, lambda: GameService._handle_ai_turn(game_id)).start()
                    
        except ValueError as e:
            logger.error(f"Error getting game state: {str(e)}")
            emit('error', {'message': str(e)})

    @socketio.on('play_card')
    def handle_play_card(data):
        game_id = data.get('game_id')
        card_index = data.get('card_index')
        if not game_id or card_index is None:
            logger.warning(f"Play card attempt with invalid data: User {current_user.id}, Data: {data}")
            emit('error', {'message': 'Game ID and card index are required'})
            return
            
        logger.info(f"User {current_user.id} playing card at index {card_index} in game {game_id}")
        try:
            result = GameService.play_card(game_id, current_user.id, card_index)
            if 'error' in result:
                logger.warning(f"Error playing card: {result['error']}")
                emit('error', {'message': result['error']})
            else:
                # Broadcast to room including sender
                emit('game_updated', result, room=game_id)
                if result.get('isGameOver'):
                    logger.info(f"Game {game_id} over, winner: {result.get('winner')}")
                    emit('game_over', {
                        'winner': result.get('winner'),
                        'game_id': game_id
                    }, room=game_id)
        except ValueError as e:
            logger.error(f"Error playing card: {str(e)}")
            emit('error', {'message': str(e)})

    @socketio.on('skip_turn')
    def handle_skip_turn(data):
        game_id = data.get('game_id')
        if not game_id:
            logger.warning(f"Skip turn attempt without game_id: User {current_user.id}")
            emit('error', {'message': 'Game ID is required'})
            return
            
        logger.info(f"User {current_user.id} skipping turn in game {game_id}")
        try:
            result = GameService.skip_turn(game_id, current_user.id)
            if 'error' in result:
                logger.warning(f"Error skipping turn: {result['error']}")
                emit('error', {'message': result['error']})
            else:
                emit('game_updated', result, room=game_id)
                if result.get('isGameOver'):
                    logger.info(f"Game {game_id} over, winner: {result.get('winner')}")
                    emit('game_over', {
                        'winner': result.get('winner'),
                        'game_id': game_id
                    }, room=game_id)
        except ValueError as e:
            logger.error(f"Error skipping turn: {str(e)}")
            emit('error', {'message': str(e)})

    @socketio.on('take_cards')
    def handle_take_cards(data):
        game_id = data.get('game_id')
        if not game_id:
            logger.warning(f"Take cards attempt without game_id: User {current_user.id}")
            emit('error', {'message': 'Game ID is required'})
            return
            
        logger.info(f"User {current_user.id} taking cards in game {game_id}")
        try:
            result = GameService.take_cards(game_id, current_user.id)
            if 'error' in result:
                logger.warning(f"Error taking cards: {result['error']}")
                emit('error', {'message': result['error']})
            else:
                emit('game_updated', result, room=game_id)
                if result.get('isGameOver'):
                    logger.info(f"Game {game_id} over, winner: {result.get('winner')}")
                    emit('game_over', {
                        'winner': result.get('winner'),
                        'game_id': game_id
                    }, room=game_id)
        except ValueError as e:
            logger.error(f"Error taking cards: {str(e)}")
            emit('error', {'message': str(e)})

    @socketio.on('start_game')
    def handle_start_game(data):
        against_ai = data.get('against_ai', True)
        logger.info(f"User {current_user.id} starting new game against AI: {against_ai}")
        try:
            game_data = GameService.create_ai_game(current_user.id) if against_ai else None
            if not game_data:
                logger.error("Failed to create game")
                emit('error', {'message': 'Failed to create game'})
                return
                
            game_id = game_data['game_id']
            join_room(game_id)
            session['game_id'] = game_id
            emit('game_created', game_data)
            
            # Get initial game state
            game_state = GameService.get_game_state(game_id, current_user.id)
            emit('game_state', game_state)
            
        except Exception as e:
            logger.error(f"Error starting game: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            emit('error', {'message': f'Error starting game: {str(e)}'})