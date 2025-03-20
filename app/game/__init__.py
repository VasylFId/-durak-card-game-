# File path: app/game/__init__.py

from flask import Blueprint

bp = Blueprint('game', __name__, url_prefix='/game')

from app.game import routes