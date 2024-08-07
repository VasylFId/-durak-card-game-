import logging
from .player import Player

logger = logging.getLogger(__name__)

class AIPlayer(Player):

  def __init__(self, name="AI"):
    super().__init__(name)
  
  def decide_move(self, game_state):
    # Implement AI logic for deciding a move
    if self.hand:
      selected_card = self.hand[0]  # Simplified logic to play the first card in hand
      logger.info(f"{self.name} decided to play {selected_card}")
      return selected_card
    else:
      return None
