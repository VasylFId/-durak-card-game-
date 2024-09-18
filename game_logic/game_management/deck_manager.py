"""
This module contains the DeckManager class, which is responsible for managing
the deck of cards in the Durak card game. It provides static methods to
reshuffle the deck, reset the trump card, draw cards for players, and obtain
information about the deck's status.
"""

import logging
from game_logic.card_package import Deck, Card

logger = logging.getLogger(__name__)


class DeckManager:

    @staticmethod
    def is_deck_empty(deck: Deck) -> bool:
        """
        Private method to check if the deck is empty.

        Returns:
            bool: True if the deck is empty, False otherwise.
        """
        return deck.is_empty()

    @staticmethod
    def __is_trump_card_drawn(deck: Deck) -> bool:
        """
        Private method to check if the trump card has been drawn.

        Returns:
            bool: True if the trump card has been drawn, False otherwise.
        """
        return deck.trump_card is None

    @staticmethod
    def can_draw_card_to_player(deck: Deck) -> bool:
        """
        Public method to check if a card can be drawn for a player.

        Returns:
            bool: True if a card can be drawn, False otherwise.
        """
        if not deck:
            logger.info("No cards can be drawn; the deck is empty.")
            return False
        return True

    @staticmethod
    def reshuffle_if_needed(deck: Deck):
        """
        Reshuffles the deck if it is not empty and logs the action.
        """
        if not deck.is_empty():
            logger.info("Reshuffling deck...")
            deck.shuffle()

    @staticmethod
    def reset_trump_card(deck: Deck) -> Card:
        """
        Resets the trump card by reshuffling the deck and drawing a new
        trump card. Logs the action and returns the new trump card.

        Returns:
            Card: The new trump card.
        """
        DeckManager.reshuffle_if_needed(deck)
        deck.set_trump_card()
        new_trump_card = deck.trump_card
        logger.info(f"New trump card set: {new_trump_card}")
        return new_trump_card

    @staticmethod
    def draw_card(deck: Deck) -> Card:
        """
        Draws a card from the deck and returns it.

        Returns:
            Card: The card drawn from the deck.
        """
        if DeckManager.can_draw_card_to_player(deck):
            drawn_card = deck.draw_card()
            logger.info(f"Card drawn: {drawn_card}")
            return drawn_card
        else:
            raise ValueError("Cannot draw a card; no more cards available.")

    @staticmethod
    def draw_trump_card(deck: Deck) -> Card:
        """
        Draws the trump card from the deck and returns it.

        Returns:
            Card: The trump card drawn from the deck.
        """
        if not DeckManager.__is_trump_card_drawn(deck):
            trump_card = deck.draw_trump_card()
            logger.info(f"Trump card drawn: {trump_card}")
            return trump_card
        else:
            logger.error("Trump card has already been drawn.")
            return None

    @staticmethod
    def get_trump_card(deck: Deck) -> Card:
        """
        Returns the current trump card in the deck.

        Returns:
            Card: The current trump card.
        """
        return deck.trump_card
