from flask import Blueprint

bp = Blueprint('game', __name__, url_prefix='/game')

from app.game import routes, events