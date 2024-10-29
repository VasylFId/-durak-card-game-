"""
This module contains the TrumpManager class, which is responsible for managing
the trump card in the game.

Classes:
    TrumpManager: A class for managing the trump card.

Usage:
    trump_manager = TrumpManager()
    trump_card_valid = trump_manager.is_trump_card_valid(deck, players)
    new_trump_card = trump_manager.set_new_trump_card(deck, players)
"""


import logging
from game_logic.card_package import Card, Deck, Rank

logger = logging.getLogger(__name__)


class TrumpManager:
    """
    A class for managing the trump card.

    Methods:
        __trump_card_is_ace(trump_card: Card) -> bool:
            Checks if the current trump card is an Ace.
        __players_have_trump(players: list, trump_card: Card) -> bool:
            Checks if any player has a card of the trump suit in their hand.
        is_trump_card_valid(deck: Deck, players: list) -> bool:
            Checks if the current trump card is valid.
        set_new_trump_card(deck: Deck, players: list) -> Card:
            Sets a new trump card by drawing the last card in the deck.
    """

    @staticmethod
    def __trump_card_is_ace(trump_card: Card) -> bool:
        """
        Checks if the current trump card is an Ace.
        """

        return trump_card.rank == Rank.ACE

    @staticmethod
    def __players_have_trump(players: list, trump_card: Card) -> bool:
        """
        Checks if any player has a card of the trump suit in their hand.

        Args:
            players (list): The list of players to check.
            trump_card (Card): The trump card to check against.

        Returns:
            bool: True if any player has a card of the trump suit, False
            otherwise.
        """

        for player in players:
            if any(card.suit == trump_card.suit for card in player.hand):
                return True
        return False

    @staticmethod
    def is_trump_card_valid(deck: Deck, players: list) -> bool:
        """
        Checks if the current trump card is valid.

        Args:
            deck (Deck): The deck of cards.
            players (list): The list of players to check.

        Returns:
            bool: True if the trump card is valid, False otherwise.
        """

        trump_card = deck.trump_card

        return not TrumpManager.__trump_card_is_ace(trump_card) and \
            TrumpManager.__players_have_trump(players, trump_card)

    @staticmethod
    def set_new_trump_card(deck: Deck, players: list) -> Card:
        """
        Sets a new trump card by drawing the last card in the deck.

        Args:
            deck (Deck): The deck of cards.

        Returns:
            Card: The new trump card.
        """

        while not TrumpManager.is_trump_card_valid(deck, players):
            deck.set_trump_card()
            new_trump_card = deck.trump_card
            logger.info(f"New trump card set: {new_trump_card}")

        return new_trump_card
