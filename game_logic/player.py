import logging
from .cards import Card, Deck

logger = logging.getLogger(__name__)

class Player:

  def __init__(self, name):
    self.name = name
    self.hand = []
  
  def draw_card(self, deck):
    card = deck.draw_card()
    self.hand.append(card)
    logger.info(f"{self.name} drew {card}")
  
  def play_card(self, card):
    if card in self.hand:
      self.hand.remove(card)
      logger.info(f"{self.name} played {card}")
      return card
    else:
      raise ValueError("Card not in hand")

  def has_cards(self):
    return len(self.hand) > 0
