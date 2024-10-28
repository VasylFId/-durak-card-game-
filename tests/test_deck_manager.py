"""
Unit tests for the DeckManager class in the Durak card game.

This module contains various tests to ensure that the DeckManager class
in the game_management module behaves as expected. It includes tests for
checking if the deck is empty, if the trump card has been drawn, if a card
can be drawn for a player, reshuffling the deck, resetting the trump card,
drawing a card, and drawing the trump card.
"""


import unittest
from game_logic.card_package import Deck, Card
from game_logic.game_management import DeckManager


class TestDeckManager(unittest.TestCase):

    def setUp(self):
        """
        Set up a new deck before each test.
        """

        # Create a new deck
        self.deck = Deck()

    def test_is_deck_empty(self):
        """
        Test the private method __is_deck_empty.
        """

        # Initially, the deck is not empty
        self.assertFalse(DeckManager.is_deck_empty(self.deck))

        # Draw all cards from the deck
        while not DeckManager.is_deck_empty(self.deck):
            self.deck.draw_card()

        # Check if the deck is empty
        self.assertTrue(DeckManager.is_deck_empty(self.deck))

    def test_is_trump_card_drawn(self):
        """
        Test the private method __is_trump_card_drawn.
        """

        # Check if the trump card has been drawn
        self.assertFalse(DeckManager._DeckManager__is_trump_card_drawn(
            self.deck))

        # Draw the trump card
        DeckManager.draw_trump_card(self.deck)

        # Check if the trump card has been drawn
        self.assertTrue(DeckManager._DeckManager__is_trump_card_drawn(
            self.deck))

    def test_can_draw_card_to_player(self):
        """
        Test the public method can_draw_card_to_player.
        """

        # Initially, the deck can draw a card
        self.assertTrue(DeckManager.can_draw_card_to_player(self.deck))

        # Draw all cards from the deck
        while DeckManager.can_draw_card_to_player(self.deck):
            self.deck.draw_card()

        # Check if the deck can draw a card
        self.assertFalse(DeckManager.can_draw_card_to_player(self.deck))

    def test_reshuffle_if_needed(self):
        """
        Test that the reshuffle_if_needed method reshuffles the deck when it's
        not empty.
        """

        # Shuffle the deck
        original_order = self.deck._Deck__cards.copy()

        # Reshuffle the deck
        DeckManager.reshuffle_if_needed(self.deck)
        reshuffled_order = self.deck._Deck__cards

        # Check if the deck has been reshuffled
        self.assertNotEqual(original_order, reshuffled_order)

    def test_reset_trump_card(self):
        """
        Test that reset_trump_card reshuffles the deck and sets a new trump
        card.
        """

        # Save the original trump card
        original_trump_card = self.deck.trump_card

        # Reset the trump card
        new_trump_card = DeckManager.reset_trump_card(self.deck)

        # Check if the trump card has been reset
        self.assertNotEqual(original_trump_card, new_trump_card)

        # Check if the new trump card has been set
        self.assertEqual(new_trump_card, self.deck.trump_card)

    def test_draw_card(self):
        """
        Test that draw_card draws a card from the deck if possible.
        """

        # Initially, the deck can draw a card
        initial_size = len(self.deck)

        # Draw a card from the deck
        drawn_card = DeckManager.draw_card(self.deck)

        # Check if the card has been drawn
        self.assertEqual(len(self.deck), initial_size - 1)

        # Check if the drawn card is an instance of Card
        self.assertIsInstance(drawn_card, Card)

    def test_draw_card_no_more_cards(self):
        """
        Test that draw_card raises an error when no more cards can be drawn.
        """

        # Draw all cards from the deck
        while DeckManager.can_draw_card_to_player(self.deck):
            self.deck.draw_card()

        # Try to draw a card from the empty deck
        with self.assertRaises(ValueError):
            DeckManager.draw_card(self.deck)

    def test_draw_trump_card(self):
        """
        Test that draw_trump_card draws the trump card from the deck.
        """

        # Initially, the trump card has not been drawn
        trump_card = DeckManager.draw_trump_card(self.deck)

        # Check if the trump card has been drawn
        self.assertIsInstance(trump_card, Card)

        # Check if the trump card has been set
        with self.assertRaises(AttributeError):
            self.assertEqual(trump_card, self.deck.trump_card)


if __name__ == '__main__':
    unittest.main()
