from enum import Enum
from functools import total_ordering
from utils.logger_setup import setup_logging

logger = setup_logging()


class Suit(Enum):
    """
    This module defines the Suit enumeration class for representing
    card suits in a card game.

    Attributes:
        HEARTS (Suit): Represents the "Hearts" suit.
        DIAMONDS (Suit): Represents the "Diamonds" suit.
        CLUBS (Suit): Represents the "Clubs" suit.
        SPADES (Suit): Represents the "Spades" suit.

    Methods:
        __str__(): Returns the string representation of the suit.

    Example:
        suit = Suit.HEARTS
        print(suit)  # Output: "♥️"
    """
    HEARTS = "♥️"
    DIAMONDS = "♦️"
    CLUBS = "♣️"
    SPADES = "♠️"

    def __str__(self):
        return self.value


@total_ordering
class Rank(Enum):
    """
    This module defines the Rank enumeration class for representing
    card ranks in a card game.

    Attributes:
        SIX (Rank): Represents the rank "6".
        SEVEN (Rank): Represents the rank "7".
        EIGHT (Rank): Represents the rank "8".
        NINE (Rank): Represents the rank "9".
        TEN (Rank): Represents the rank "10".
        JACK (Rank): Represents the rank "J".
        QUEEN (Rank): Represents the rank "Q".
        KING (Rank): Represents the rank "K".
        ACE (Rank): Represents the rank "A".

    Methods:
        __str__(): Returns the string representation of the rank.

    Example:
        rank = Rank.SIX
        print(rank)  # Output: "6"
    """
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

    def __repr__(self) -> str:
        return str(self)

    def __gt__(self, other):
        rank_order = list(Rank)
        return rank_order.index(self) > rank_order.index(other)

    def __lt__(self, other):
        rank_order = list(Rank)
        return rank_order.index(self) < rank_order.index(other)

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)
