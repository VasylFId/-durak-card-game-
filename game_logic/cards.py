from enum import Enum
import random
import logging

logger = logging.getLogger(__name__)

class Suit(Enum):
    HEARTS = "♥️"
    DIAMONDS = "♦️"
    CLUBS = "♣️"
    SPADES = "♠️"

    def __str__(self):
        return self.value

class Rank(Enum):
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

    def __str__(self):
        return self.value
class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
        self.weight = self.calculate_weight()

    def calculate_weight(self):
        rank_weights = {
            Rank.SIX: 6, Rank.SEVEN: 7, Rank.EIGHT: 8, Rank.NINE: 9,
            Rank.TEN: 10, Rank.JACK: 11, Rank.QUEEN: 12, Rank.KING: 13,
            Rank.ACE: 14
        }
        return rank_weights[self.rank]

    def is_trump(self, trump_suit: Suit) -> bool:
        return self.suit == trump_suit

    def compare(self, other_card: 'Card', trump_suit: Suit) -> int:
        logger.info(f"Comparing {self} (Trump: {self.is_trump(trump_suit)}) "
                    f"with {other_card} (Trump: {other_card.is_trump(trump_suit)})")

        # Case 1: Both cards are trump cards
        if self.is_trump(trump_suit) and other_card.is_trump(trump_suit):
            return self.weight - other_card.weight

        # Case 2: One card is a trump card
        if self.is_trump(trump_suit):
            return 1  # self wins
        if other_card.is_trump(trump_suit):
            return -1  # other_card wins

        # Case 3: Neither card is a trump card, compare by suit first
        if self.suit == other_card.suit:
            return self.weight - other_card.weight
        else:
            return 0  # Different suits and neither is trump, consider them equal for this game

    def __repr__(self):
        return f"{self.suit.value}{self.rank.value}"

    def __lt__(self, other):
        return self.weight < other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __eq__(self, other):
        return self.weight == other.weight and self.suit == other.suit

class DeckManager:
    def __init__(self, deck: Deck):
        self.deck = deck

    def reshuffle_if_needed(self):
        if len(self.deck.cards) > 0:
            logger.info("Reshuffling deck...")
            self.deck.shuffle()

    def draw_cards(self, players: list):
        for player in players:
            self.ensure_sufficient_cards_in_hand(player)

    def ensure_sufficient_cards_in_hand(self, player):
        while len(player.hand) < 6 and not self.deck.is_empty():
            drawn_card = self.deck.draw_card()
            player.hand.append(drawn_card)
            logger.info(f"{player.name} drew {drawn_card}")
        player.sort_hand()

    def check_trump_distribution(self, players):
        # No longer needed in DeckManager, handled by TrumpManager
        pass
