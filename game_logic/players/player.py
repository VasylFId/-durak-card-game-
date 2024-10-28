"""
This module defines the Player class, which represents a player in the
Durak card game.

Classes:
    Player: A class representing a player in the game.

Usage:
    player = Player("Alice")
    player.add_card_to_hand(card)
    player.remove_card_from_hand(card)
    hand = player.show_hand()
    player.update_trump_suit(new_trump_suit)
    has_cards = player.has_cards()
"""

import logging
from game_logic.card_package import Card, Suit

logger = logging.getLogger(__name__)


class Player:
    """
    A class representing a player in the Durak card game.

    Attributes:
        name (str): The name of the player.
        hand (list of Card): The list of cards in the player's hand.
        trump_suit (Suit): The trump suit for the player.

    Methods:
        add_card_to_hand(card: Card): Adds a card to the player's hand.
        remove_card_from_hand(card: Card) -> bool: Removes a card from the
                                                    player's hand.
        show_hand() -> list: Returns the player's current hand.
        update_trump_suit(new_trump_suit: Suit): Updates the trump suit for
                                                 the player.
        has_cards() -> bool: Checks if the player has any cards left in their
                             hand.
    """

    def __init__(self, name: str):
        """
        Initializes the player with a name, an empty hand, and no trump suit.

        Args:
            name (str): The name of the player.
        """

        self.name = name
        self.hand = []
        self.trump_suit = None  # Initially, the trump suit is not set.

    def add_card_to_hand(self, card: Card):
        """
        Adds a card to the player's hand and sorts the hand automatically.

        Args:
            card (Card): The card to add to the hand.
        """

        self.hand.append(card)
        logger.info(f"{self.name} added {card} to their hand")
        self.__sort_hand()

    def remove_card_from_hand(self, card: Card) -> bool:
        """
        Removes a card from the player's hand.

        Args:
            card (Card): The card to remove from the hand.

        Returns:
            bool: True if the card was removed, False if it was not found.
        """

        if card in self.hand:
            self.hand.remove(card)
            logger.info(f"{self.name} removed {card} from their hand")
            return True
        else:
            logger.info(f"{self.name} tried to remove {card}, "
                        "but it was not found in hand")
            return False

    def show_hand(self) -> list:
        """
        Returns the player's current hand.

        Returns:
            list: The sorted hand of the player.
        """

        return self.hand

    def __sort_hand(self):
        """
        Sorts the player's hand with trump cards first, in descending order,
        followed by non-trump cards in descending order of rank, ignoring
        suits.
        """

        if self.trump_suit:
            # Separate trump and non-trump cards
            trump_cards = [card
                           for card in self.hand
                           if card.is_trump(self.trump_suit)]
            non_trump_cards = [card
                               for card in self.hand
                               if not card.is_trump(self.trump_suit)]

            # Sort trump cards by descending rank
            trump_cards.sort(key=lambda card: card.weight, reverse=True)

            # Sort non-trump cards by descending rank
            non_trump_cards.sort(key=lambda card: card.weight, reverse=True)

            # Combine the sorted lists
            self.hand = trump_cards + non_trump_cards
        else:
            # Sort all cards by descending rank, ignoring suit
            self.hand.sort(key=lambda card: card.weight, reverse=True)

        logger.info(f"{self.name}'s sorted hand: {self.hand}")

    def update_trump_suit(self, new_trump_suit: Suit):
        """
        Updates the trump suit for the player and re-sorts the hand.

        Args:
            new_trump_suit (Suit): The new trump suit.
        """

        self.trump_suit = new_trump_suit
        self.__sort_hand()
        logger.info(f"{self.name}'s trump suit updated to {self.trump_suit}")

    def has_cards(self):
        """
        Checks if the player has any cards left in their hand.

        Returns:
            bool: True if the player has cards, False otherwise.
        """

        return len(self.hand) > 0
