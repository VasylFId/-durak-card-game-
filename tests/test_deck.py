"""
Unit tests for the Deck class in the Durak card game.

This module contains various tests to ensure that the Deck class
in the card_package module behaves as expected. It includes tests
for initializing the deck, shuffling, drawing, returning cards,
and managing the trump card.
"""

import unittest
from game_logic.card_package import Deck, Card


class TestDeck(unittest.TestCase):

    def setUp(self):
        """Initialize a new Deck instance for each test."""

        self.deck = Deck()

    def test_deck_initialization(self):
        """Test that the deck initializes with the correct number of
        cards and sets a trump card."""

        self.assertEqual(len(self.deck), 35)  # 36 cards, 1 is trump
        self.assertIsInstance(self.deck.trump_card, Card)
        self.assertFalse(self.deck._Deck__trump_card_drawn)

    def test_draw_card(self):
        """Test drawing a card from the deck reduces the deck size."""

        initial_size = len(self.deck)
        card = self.deck.draw_card()

        # Check that the card is not None and the deck size is reduced
        self.assertEqual(len(self.deck), initial_size - 1)
        self.assertIsInstance(card, Card)

    def test_draw_all_cards(self):
        """Test drawing all cards including the trump card leaves the
        deck empty."""

        while self.deck:  # Draw all but one (trump card) from the deck.
            self.deck.draw_card()

        self.assertTrue(self.deck.is_empty())
        # Deck should be empty,
        # trump card is still there.

        # Draw the trump card and now deck should be empty
        self.deck.draw_trump_card()
        self.assertTrue(self.deck.is_empty())

    def test_draw_trump_card(self):
        """Test that drawing the trump card sets the flag and returns
        the correct card."""

        deck_trump_card = self.deck.trump_card
        trump_card = self.deck.draw_trump_card()

        # Trump card should be the same as the one drawn
        self.assertEqual(trump_card, deck_trump_card)
        self.assertTrue(self.deck._Deck__trump_card_drawn)

        # Trump card should be None in the deck now
        self.assertIsNone(self.deck.trump_card)

        # Attempt to draw the trump card again should return None
        self.assertIsNone(self.deck.draw_trump_card())

    def test_return_card_to_deck(self):
        """Test returning a card to the deck increases its size and
        shuffles correctly."""

        card = self.deck.draw_card()
        initial_size = len(self.deck)

        # Return the card to the deck
        self.deck.return_card(card)

        # Deck size should increase by 1
        self.assertEqual(len(self.deck), initial_size + 1)

    def test_set_trump_card(self):
        """Test that setting a new trump card works as expected."""

        initial_trump = self.deck.trump_card
        self.deck.set_trump_card()
        new_trump = self.deck.trump_card

        # New trump card should not be the same as the initial one
        self.assertNotEqual(initial_trump, new_trump)

        # Trump card should be set
        self.assertFalse(self.deck._Deck__trump_card_drawn)

    def test_iter(self):
        """Test that the deck is iterable."""

        # Check that all cards are instances of Card
        for card in self.deck:
            self.assertIsInstance(card, Card)


if __name__ == '__main__':
    unittest.main()
