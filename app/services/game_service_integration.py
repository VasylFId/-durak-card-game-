# app/services/game_service_integration.py

import logging
import json
from flask import session
from flask_socketio import emit, join_room
from flask_login import current_user
from app.services.game_service import GameService, ACTIVE_GAMES

logger = logging.getLogger(__name__)

def connect_game_socket_events(socketio):
    """
    Connect all the socket events needed for game interaction
    This function should be called when initializing the app
    """
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection to socket"""
        if current_user.is_authenticated:
            logger.info(f"Client connected: User {current_user.id}")
            emit('connection_response', {'status': 'connected', 'user_id': current_user.id})
        else:
            logger.warning(f"Unauthenticated client connection attempt")
            emit('connection_response', {'status': 'error', 'message': 'Authentication required'})
    
    @socketio.on('join_game')
    def handle_join_game(data):
        """Handle player joining a game"""
        game_id = data.get('game_id')
        if not game_id:
            logger.warning(f"Join game attempt without game_id: User {current_user.id}")
            emit('error', {'message': 'Game ID is required'})
            return
            
        logger.info(f"User {current_user.id} joining game {game_id}")
        
        # Join the Socket.IO room for this game
        join_room(game_id)
        
        # Notify other players that someone joined
        emit('player_joined', {
            'user_id': current_user.id,
            'username': current_user.username
        }, room=game_id, include_self=False)
        
        # Get and send the current game state
        try:
            game_state = GameService.get_game_state(game_id, current_user.id)
            emit('game_state', game_state)
        except ValueError as e:
            logger.error(f"Error getting game state: {str(e)}")
            emit('error', {'message': str(e)})
    
    @socketio.on('play_card')
    def handle_play_card(data):
        """Handle player playing a card"""
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
                # Broadcast the updated game state to all players in the room
                emit('game_updated', result, room=game_id)
                
                # Check if game is over
                if result.get('isGameOver'):
                    logger.info(f"Game {game_id} over, winner: {result.get('winner')}")
                    emit('game_over', {
                        'winner': result.get('winner'),
                        'game_id': game_id
                    }, room=game_id)
                    
                    # You might want to update statistics here or when ending the game
        except ValueError as e:
            logger.error(f"Error playing card: {str(e)}")
            emit('error', {'message': str(e)})
    
    @socketio.on('skip_turn')
    def handle_skip_turn(data):
        """Handle player skipping their turn"""
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
        """Handle player taking cards"""
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
        """Handle starting a new game"""
        against_ai = data.get('against_ai', True)
        
        logger.info(f"User {current_user.id} starting new game against AI: {against_ai}")
        
        try:
            # For now, focusing on AI games
            game_data = GameService.create_ai_game(current_user.id) if against_ai else None
            
            if not game_data:
                logger.error("Failed to create game")
                emit('error', {'message': 'Failed to create game'})
                return
                
            game_id = game_data['game_id']
            
            # Join the room for the new game
            join_room(game_id)
            
            # Store the game ID in the session
            session['game_id'] = game_id
            
            # Inform the client about the created game
            emit('game_created', game_data)
            
            # Send the initial game state
            game_state = GameService.get_game_state(game_id, current_user.id)
            emit('game_state', game_state)
            
        except Exception as e:
            logger.error(f"Error starting game: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            emit('error', {'message': f'Error starting game: {str(e)}'})