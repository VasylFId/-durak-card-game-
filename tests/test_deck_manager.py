import unittest
from game_logic.card_package import Deck, Card
from game_logic.game_management import DeckManager

class TestDeckManager(unittest.TestCase):

    def setUp(self):
        """
        Set up a new deck before each test.
        """
        self.deck = Deck()

    def test_is_deck_empty(self):
        """
        Test the private method __is_deck_empty.
        """
        self.assertFalse(DeckManager.is_deck_empty(self.deck))
        while not DeckManager.is_deck_empty(self.deck):
            self.deck.draw_card()
        self.assertTrue(DeckManager.is_deck_empty(self.deck))

    def test_is_trump_card_drawn(self):
        """
        Test the private method __is_trump_card_drawn.
        """
        self.assertFalse(DeckManager._DeckManager__is_trump_card_drawn(self.deck))
        DeckManager.draw_trump_card(self.deck)
        self.assertTrue(DeckManager._DeckManager__is_trump_card_drawn(self.deck))

    def test_can_draw_card_to_player(self):
        """
        Test the public method can_draw_card_to_player.
        """
        self.assertTrue(DeckManager.can_draw_card_to_player(self.deck))
        while DeckManager.can_draw_card_to_player(self.deck):
            self.deck.draw_card()
        self.assertFalse(DeckManager.can_draw_card_to_player(self.deck))

    def test_reshuffle_if_needed(self):
        """
        Test that the reshuffle_if_needed method reshuffles the deck when it's not empty.
        """
        original_order = self.deck._Deck__cards.copy()
        DeckManager.reshuffle_if_needed(self.deck)
        reshuffled_order = self.deck._Deck__cards
        self.assertNotEqual(original_order, reshuffled_order)

    def test_reset_trump_card(self):
        """
        Test that reset_trump_card reshuffles the deck and sets a new trump card.
        """
        original_trump_card = self.deck.trump_card
        new_trump_card = DeckManager.reset_trump_card(self.deck)
        self.assertNotEqual(original_trump_card, new_trump_card)
        self.assertEqual(new_trump_card, self.deck.trump_card)

    def test_draw_card(self):
        """
        Test that draw_card draws a card from the deck if possible.
        """
        initial_size = len(self.deck)
        drawn_card = DeckManager.draw_card(self.deck)
        self.assertEqual(len(self.deck), initial_size - 1)
        self.assertIsInstance(drawn_card, Card)

    def test_draw_card_no_more_cards(self):
        """
        Test that draw_card raises an error when no more cards can be drawn.
        """
        while DeckManager.can_draw_card_to_player(self.deck):
            self.deck.draw_card()

        with self.assertRaises(ValueError):
            DeckManager.draw_card(self.deck)

    def test_draw_trump_card(self):
        """
        Test that draw_trump_card draws the trump card from the deck.
        """
        trump_card = DeckManager.draw_trump_card(self.deck)
        self.assertIsInstance(trump_card, Card)

        with self.assertRaises(AttributeError):
            self.assertEqual(trump_card, self.deck.trump_card)


if __name__ == '__main__':
    unittest.main()
