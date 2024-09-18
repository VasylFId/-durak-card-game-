from .suit_rank import Suit, Rank
import logging

logger = logging.getLogger(__name__)


class Card:
    """
    Represents a playing card in the game.

    Attributes:
        suit (Suit): The suit of the card (Hearts, Diamonds, Clubs, Spades).
        rank (Rank): The rank of the card (Six, Seven, Eight, etc.).
        weight (int): The weight of the card, based on its rank.

    Methods:
        calculate_weight(): Determines the weight of the card based
                            on its rank.
        is_trump(trump_suit: Suit) -> bool: Checks if the card is a
                                            trump card.
        compare(other_card: 'Card', trump_suit: Suit) -> int:
            Compares this card with another card, considering the
            trump suit.
        __repr__(): Returns the string representation of the card.
        __lt__(other: 'Card') -> bool: Less-than comparison based on
                                       weight and suit.
        __gt__(other: 'Card') -> bool: Greater-than comparison based
                                       on weight and suit.
        __eq__(other: 'Card') -> bool: Equality comparison based on
                                       weight and suit.
    """

    def __init__(self, suit: Suit, rank: Rank):
        """
        Initializes a Card instance with a suit, rank, and calculates
        its weight.

        Args:
            suit (Suit): The suit of the card.
            rank (Rank): The rank of the card.
        """
        self.__suit = suit
        self.__rank = rank
        self.__weight = self.__calculate_weight()

    def __calculate_weight(self) -> int:
        """
        Calculates the weight of the card based on its rank.

        Returns:
            int: The weight of the card.
        """
        rank_weights = {
            Rank.SIX: 6, Rank.SEVEN: 7, Rank.EIGHT: 8, Rank.NINE: 9,
            Rank.TEN: 10, Rank.JACK: 11, Rank.QUEEN: 12, Rank.KING: 13,
            Rank.ACE: 14
        }
        return rank_weights[self.rank]

    @property
    def suit(self):
        """
        Property that returns the suit of the card.

        Returns:
            Suit: The suit of the card (e.g., Hearts, Diamonds, Clubs,
            Spades).
        """
        return self.__suit

    @property
    def rank(self):
        """
        Property that returns the rank of the card.

        Returns:
            Rank: The rank of the card (e.g., Ace, 2, 3, ..., King).
        """
        return self.__rank

    @property
    def weight(self):
        """
        Property that returns the weight of the card.

        Returns:
            int: The weight of the card, used for game logic (e.g.,
            determining the strength of the card).
        """
        return self.__weight

    def is_trump(self, trump_suit: Suit) -> bool:
        """
        Checks if the card is a trump card.

        Args:
            trump_suit (Suit): The suit designated as trump.

        Returns:
            bool: True if this card is a trump card, False otherwise.
        """
        return self.suit == trump_suit

    def compare(self, other_card: 'Card', trump_suit: Suit) -> int:
        """
        Compares this card with another card, taking into account
        the trump suit.

        Args:
            other_card (Card): The card to compare with.
            trump_suit (Suit): The suit designated as trump.

        Returns:
            int: Positive if this card wins, negative if the other
                 card wins, zero if they are considered equal.
        """
        logger.info(
            f"Comparing {self} (Trump: {self.is_trump(trump_suit)}) "
            f"with {other_card} (Trump: {other_card.is_trump(trump_suit)})"
        )

        if self.is_trump(trump_suit) and other_card.is_trump(trump_suit):
            return self.weight - other_card.weight

        if self.is_trump(trump_suit):
            return 1  # self wins
        if other_card.is_trump(trump_suit):
            return -1  # other_card wins

        if self.suit == other_card.suit:
            return self.weight - other_card.weight
        else:
            return 0  # Different suits and neither is trump

    def __repr__(self) -> str:
        """
        Returns the string representation of the card.

        Returns:
            str: The string representation of the card.
        """
        return f"{self.suit.value}{self.rank.value}"

    def __lt__(self, other: 'Card') -> bool:
        """
        Compares if this card is less than another card based on
        weight and suit.

        Args:
            other (Card): The card to compare with.

        Returns:
            bool: True if this card is less than the other card,
                  False otherwise.
        """
        return self.weight < other.weight

    def __gt__(self, other: 'Card') -> bool:
        """
        Compares if this card is greater than another card based on
        weight and suit.

        Args:
            other (Card): The card to compare with.

        Returns:
            bool: True if this card is greater than the other card,
                  False otherwise.
        """
        return self.weight > other.weight

    def __eq__(self, other: 'Card') -> bool:
        """
        Compares if this card is equal to another card based on
        weight and suit.

        Args:
            other (Card): The card to compare with.

        Returns:
            bool: True if this card is equal to the other card,
                  False otherwise.
        """
        return self.weight == other.weight and self.suit == other.suit
