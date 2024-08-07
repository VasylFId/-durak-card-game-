import logging
from .player import Player
from .ai import AIPlayer
from .cards import Deck

logger = logging.getLogger(__name__)

class DurakGame:

  def __init__(self):
    self.players = []
    self.deck = Deck()
    self.trump_suit = None
    self.active_player_index = 0
  
  def start_game(self):
    self.deck.shuffle()
    self.trump_suit = self.deck.draw_card().suit
    self.deck.return_card(self.trump_suit)
    logger.info(f"Trump suit is {self.trump_suit}")
    self.deal_cards()

  def deal_cards(self):
    for player in self.players:
      for _ in range(6):
        player.draw_card(self.deck)
  
  def add_player(self, player):
    if isinstance(player, Player):
      self.players.append(player)
    else:
      raise ValueError("Only instances of Player can be added.")
  
  def next_turn(self):
    # Logic to handle the next turn in the game
    self.active_player_index = (self.active_player_index + 1) % len(self.players)
  
  def is_game_over(self):
    # Implement logic to check if the game is over
    pass

  def determine_winner(self):
    # Implement logic to determine the winner of the game
    pass
