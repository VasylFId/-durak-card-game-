"""
This module defines the Deck class, which represents a deck of cards
for the Durak card game.

Classes:
    Deck: A class representing a deck of cards used in the game.

Usage:
    deck = Deck()
    card = deck.draw_card()
    deck.return_card(card)
    trump_card = deck.draw_trump_card()
"""

import random
import logging
from .suit_rank import Suit, Rank
from .card import Card

logger = logging.getLogger(__name__)


class Deck:
    """
    A class representing a deck of cards used in the Durak card game.

    Attributes:
        __cards (list of Card): The list of cards in the deck.
        __trump_card (Card): The trump card for the game.

    Methods:
        shuffle(): Shuffles the deck of cards.
        draw_card() -> Card: Draws a card from the deck.
        return_card(card: Card): Returns a card to the deck at a random
                                 position.
        set_trump_card(): Sets the trump card by drawing the last card in the
                          deck.
        is_empty() -> bool: Checks if the deck is empty.
        draw_trump_card() -> Card: Returns the trump card.
    """

    def __init__(self):
        """
        Initializes the deck with 36 cards, shuffles the deck, and sets the
        trump card.
        """

        self.__cards = [Card(suit, rank) for suit in Suit for rank in Rank]
        self.__trump_card = None
        self.__trump_card_drawn = False
        self.shuffle()
        self.set_trump_card()

    def shuffle(self) -> None:
        """
        Shuffles the deck of cards and logs the action.
        """

        random.shuffle(self.__cards)
        logger.info("Deck shuffled")

    def draw_card(self) -> Card:
        """
        Draws a card from the deck.

        Returns:
            Card: The card drawn from the deck.

        Raises:
            ValueError: If the deck is empty.
        """

        if self.__cards:
            return self.__cards.pop()
        else:
            raise ValueError("The deck is empty")

    def return_card(self, card: Card) -> None:
        """
        Returns a card to the deck at a random position and logs the action.

        Args:
            card (Card): The card to be returned to the deck.
        """

        position = random.randint(0, len(self.__cards))
        self.__cards.insert(position, card)
        logger.info(f"Card {card} returned to the deck at position {position}")

    def set_trump_card(self) -> None:
        """
        Sets the trump card by drawing the last card from the deck.
        """

        self.__trump_card = self.draw_card()
        logger.info(f"Trump card set: {self.trump_card}")

    def is_empty(self) -> bool:
        """
        Checks if the deck is empty.

        Returns:
            bool: True if the deck is empty, False otherwise.
        """

        return len(self.__cards) == 0

    @property
    def trump_card(self):
        """
        Property that returns the trump card.

        Returns:
            Card: The trump card.
        """

        return self.__trump_card

    def draw_trump_card(self) -> Card:
        """
        Draws the trump card from the deck. If the trump card has already been
        drawn, returns None.

        Returns:
            Card: The trump card or None if it has already been drawn.
        """

        if self.__trump_card_drawn:
            logger.warning("Trump card has already been drawn.")
            return None
        else:
            self.__trump_card_drawn = True
            card = self.__trump_card
            self.__trump_card = None  # Reset trump card after drawing
            return card

    def set_custom_deck(self, custom_deck_cards: list):
        """
        Sets the deck of cards to a custom deck.
        This method is going to be used only for testing purposes.

        Args:
            custom_deck_cards (list of Card): The custom deck of cards.
        """

        self.__cards = []
        self.__cards.extend(custom_deck_cards)
        logger.info("Resetting trump card...")
        self.shuffle()
        self.set_trump_card()
        logger.info("Custom deck set.")

    def __iter__(self):
        """
        Returns an iterator for the deck of cards.

        Returns:
            iter: An iterator for the deck of cards.
        """

        return iter(self.__cards)

    def __contains__(self, check__card: Card):
        """
        Checks if the deck contains a specific card.

        Args:
            card (Card): The card to check.

        Returns:
            bool: True if the card is in the deck, False otherwise.
        """

        for card in self.__cards:
            if card == check__card:
                return True
        return False

    def __len__(self):
        """
        Returns the number of cards left in the deck.

        Returns:
            int: The number of cards remaining in the deck.
        """

        return len(self.__cards)

    def __repr__(self) -> str:
        """
        Returns the string representation of the deck.

        Returns:
            str: The string representation of the deck.
        """

        return f"Deck({len(self.__cards)} cards remaining).\n" + \
               f"Trump card: {self.trump_card}\n" + \
               f"Cards remaining: {self.__cards}"
