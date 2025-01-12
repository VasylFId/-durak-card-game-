# """
# Unit tests for the Deck class in the Durak card game.

# This module contains unit tests for the Deck class, which is a part
# of the card_package module. These tests ensure that the Deck class
# functions as expected, including tests for deck initialization,
# card drawing, shuffling, and card returning.

# """

# import unittest
# from game_logic.card_package import Deck
# from utils.logger_setup import setup_logging

# # Setup logging before any tests
# setup_logging()


# class TestDeckStatic(unittest.TestCase):
#     """
#     Unit tests for the Deck class.
#     """

#     def setUp(self):
#         """
#         Initialize a new Deck instance for each test.
#         """
#         self.deck = Deck()

#     def test_initial_deck_size(self):
#         """
#         Test that the deck is initialized with 35 cards, accounting for
#         the trump card being removed from the deck.
#         """
#         self.assertEqual(len(self.deck), 35)

#     def test_draw_card(self):
#         """
#         Test that drawing a card from the deck reduces the deck size and
#         returns a valid card.
#         """
#         initial_size = len(self.deck)
#         card = self.deck.draw_card()
#         self.assertIsNotNone(card)
#         self.assertEqual(len(self.deck), initial_size - 1)

#     def test_shuffle_deck(self):
#         """
#         Test that shuffling the deck changes the order of the cards.
#         """
#         # Accessing private attribute
#         original_order = self.deck._Deck__cards[:]
#         self.deck.shuffle()
#         # Check that order has changed
#         self.assertNotEqual(self.deck._Deck__cards, original_order)

#     def test_draw_all_cards(self):
#         """
#         Test that all cards can be drawn from the deck, and that the deck
#         is correctly identified as empty afterward.
#         """
#         while not self.deck.is_empty():
#             self.deck.draw_card()
#         self.assertTrue(self.deck.is_empty())

#     def test_return_card(self):
#         """
#         Test that a card can be returned to the deck and is present in
#         the deck afterward.
#         """
#         card = self.deck.draw_card()
#         self.deck.return_card(card)
#         # Accessing private attribute
#         self.assertIn(card, self.deck._Deck__cards)


# if __name__ == '__main__':
#     unittest.main()
