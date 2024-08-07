import logging
import random
from enum import Enum

logger = logging.getLogger(__name__)

class Suit(Enum):
  HEARTS = 'Hearts'
  DIAMONDS = 'Diamonds'
  CLUBS = 'Clubs'
  SPADES = 'Spades'

class Rank(Enum):
  SIX = '6'
  SEVEN = '7'
  EIGHT = '8'
  NINE = '9'
  TEN = '10'
  JACK = 'J'
  QUEEN = 'Q'
  KING = 'K'
  ACE = 'A'

class Card:

  def __init__(self, suit, rank):
    self.suit = suit
    self.rank = rank

  def __repr__(self):
    return f"{self.rank.value} of {self.suit.value}"

class Deck:

  def __init__(self):
    self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]
  
  def shuffle(self):
    random.shuffle(self.cards)
    logger.info("Deck shuffled")
  
  def draw_card(self):
    if self.cards:
      return self.cards.pop()
    else:
      raise ValueError("The deck is empty")

  def return_card(self, card):
    self.cards.insert(0, card)
    logger.info(f"Card {card} returned to the deck")
