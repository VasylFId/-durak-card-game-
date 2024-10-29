"""
Unit tests for the TrumpManager class. The TrumpManager class is responsible
for managing the trump card in the game.

This module contains various tests to ensure that the TrumpManager class is
working as expected. It includes tests to check if the trump card is an Ace, if
any player has a trump card, if the current trump card is valid, and if a new
trump card can be set.
"""


import logging
import unittest
from game_logic.game_management import DeckManager, TrumpManager
from game_logic.card_package import Deck, Card, Suit, Rank
from game_logic.players import Player

logger = logging.getLogger(__name__)


class TestTrumpManager(unittest.TestCase):
    def setUp(self):
        """
        Initialize DeckManager, TrumpManager, and Player instances for each
        test. Remove assigned cards from the deck.
        """

        # Initialize the deck, deck manager, and players
        self.deck = Deck()

        # Set the trump card
        self.deck.return_card(self.deck.trump_card)
        self.deck_Deck_trump_card = None

        # Create a deck manager
        self.deck_manager = DeckManager()

        # Create two players
        self.player1 = Player(name="Alice")
        self.player2 = Player(name="Bob")
        self.players = [self.player1, self.player2]

        # Predefine the cards and assign them to the players
        self.player1.hand = [
            Card(Suit.DIAMONDS, Rank.ACE),     # ♦️A
            Card(Suit.CLUBS, Rank.ACE),        # ♣️A
            Card(Suit.CLUBS, Rank.KING),       # ♣️K
            Card(Suit.HEARTS, Rank.KING),      # ♥️K
            Card(Suit.DIAMONDS, Rank.QUEEN),   # ♦️Q
            Card(Suit.CLUBS, Rank.QUEEN)       # ♣️Q
        ]

        self.player2.hand = [
            Card(Suit.DIAMONDS, Rank.KING),    # ♦️K
            Card(Suit.CLUBS, Rank.JACK),       # ♣️J
            Card(Suit.CLUBS, Rank.TEN),        # ♣10
            Card(Suit.HEARTS, Rank.QUEEN),     # ♥️Q
            Card(Suit.DIAMONDS, Rank.JACK),    # ♦️J
            Card(Suit.CLUBS, Rank.NINE)        # ♣️9
        ]

        logger.info("\n\nInitial deck: %s", self.deck)

        # Remove the assigned cards from the deck
        for player in self.players:
            for card in player.hand:
                if card in self.deck:
                    self.deck._Deck__cards.remove(card)

        # Set the trump card
        self.deck.set_trump_card()

        logger.info("\n\nDeck after removing assigned cards: %s", self.deck)

    def test_trump_card_is_ace(self):
        """
        Test the private method __trump_card_is_ace.
        """

        # Assign a card with the rank of Ace
        ace_of_spades = Card(Suit.SPADES, Rank.ACE)  # ♠️A

        # Test when the trump card is an Ace
        self.assertTrue(
            TrumpManager._TrumpManager__trump_card_is_ace(ace_of_spades)
        )

        # Assign a card with the rank of King
        non_ace = Card(Suit.HEARTS, Rank.KING)       # ♥️K

        # Test when the trump card is not an Ace
        self.assertFalse(
            TrumpManager._TrumpManager__trump_card_is_ace(non_ace)
        )

    def test_players_have_trump(self):
        """
        Test the private method __players_have_trump that checks if any player
        has a card of the trump suit in their hand.
        """

        trump_card = Card(Suit.SPADES, Rank.TEN)   # ♠️10

        # Test when no player has a trump card
        self.assertFalse(
            TrumpManager._TrumpManager__players_have_trump(self.players,
                                                           trump_card)
                        )

        # Test when one player has a trump card
        self.player1.hand.append(trump_card)
        self.assertTrue(TrumpManager._TrumpManager__players_have_trump(
            self.players,
            trump_card)
        )

        # Test when both players have a trump card
        self.player2.hand.append(trump_card)
        self.assertTrue(
            TrumpManager._TrumpManager__players_have_trump(self.players,
                                                           trump_card)
                        )

    def test_is_trump_card_valid(self):
        """
        Test the public method is_trump_card_valid.
        """
        trump_card = Card(Suit.SPADES, Rank.ACE)  # ♠️A

        self.deck._Deck__trump_card = trump_card

        if trump_card in self.deck:
            self.deck._Deck__cards.remove(trump_card)

        # Test when the trump card is an Ace and no player has a trump card
        self.assertFalse(TrumpManager.is_trump_card_valid(self.deck, self.players))
        logger.info(self.deck)

        # Test when the trump card is an Ace and one player has a trump card
        self.player1.hand.append(trump_card)
        self.assertFalse(TrumpManager.is_trump_card_valid(self.deck, self.players))

        # Test when the trump card is an Ace and both players have a trump card
        self.player2.hand.append(trump_card)
        self.assertFalse(TrumpManager.is_trump_card_valid(self.deck, self.players))

        # Test when the trump card is not an Ace and no player has a trump card
        self.player1.hand.remove(trump_card)
        self.player2.hand.remove(trump_card)

        trump_card = Card(Suit.SPADES, Rank.TEN) # ♠️10

        self.deck.return_card(self.deck.trump_card)
        self.deck_Deck_trump_card = None
        self.deck._Deck__trump_card = trump_card

        self.assertFalse(TrumpManager.is_trump_card_valid(self.deck, self.players))

        # Test when the trump card is not an Ace and one player has a trump card
        self.player1.hand.append(trump_card)
        logger.info(self.player1.hand)
        logger.info(self.deck)
        self.assertTrue(TrumpManager.is_trump_card_valid(self.deck, self.players))

        # Test when the trump card is not an Ace and both players have a trump card
        self.player2.hand.append(trump_card)
        self.assertTrue(TrumpManager.is_trump_card_valid(self.deck, self.players))

    def test_set_new_trump_card(self):
        """
        Test the public method set_new_trump_card.
        """
        trump_card = Card(Suit.SPADES, Rank.ACE)  # ♠️A

        self.deck._Deck__trump_card = trump_card

        if trump_card in self.deck:
            self.deck._Deck__cards.remove(trump_card)

        logger.info("\n\nTest when the current trump card is an Ace:\n")
        # Test when the current trump card is an Ace
        new_trump_card = TrumpManager.set_new_trump_card(self.deck, self.players)
        self.assertNotEqual(trump_card, new_trump_card)
        self.assertEqual(new_trump_card, self.deck.trump_card)

        logger.info("\n\nTest when the current trump card is not an Ace:\n")
        # Test when the current trump card is not an Ace
        trump_card = Card(Suit.SPADES, Rank.TEN)  # ♠️10

        self.deck.return_card(self.deck.trump_card)
        self.deck_Deck_trump_card = None
        self.deck._Deck__trump_card = trump_card

        new_trump_card = TrumpManager.set_new_trump_card(self.deck, self.players)
        self.assertNotEqual(trump_card, new_trump_card)
        self.assertEqual(new_trump_card, self.deck.trump_card)


if __name__ == '__main__':
    unittest.main()
