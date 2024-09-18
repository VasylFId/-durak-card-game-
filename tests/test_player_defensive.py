import unittest
from game_logic.players import Player
from game_logic.card_package import Card, Suit, Rank
from utils.logger_setup import setup_logging

# Setup logging before any tests
setup_logging()


class TestPlayerDefensive(unittest.TestCase):
    def setUp(self):
        """
        Initialize a Player instance named "Bob" before each test.
        """
        self.player = Player(name="Bob")

    def test_defensive_behavior(self):
        """
        Test that a defensive player holds onto trump cards and plays
        non-trump cards first.
        """
        card1 = Card(Suit.HEARTS, Rank.SIX)
        card2 = Card(Suit.SPADES, Rank.KING)
        card3 = Card(Suit.CLUBS, Rank.ACE)

        self.player.add_card_to_hand(card1)
        self.player.add_card_to_hand(card2)
        self.player.add_card_to_hand(card3)

        # Defensive players might want to hold onto trump cards
        self.player.update_trump_suit(Suit.CLUBS)
        expected_order = [card3, card2, card1]  # Trump card first, then others
        self.assertEqual(self.player.show_hand(), expected_order)

    def test_defend_with_lowest_card(self):
        """
        Test that a defensive player defends with the lowest possible card
        first.
        """
        card1 = Card(Suit.HEARTS, Rank.SIX)
        card2 = Card(Suit.HEARTS, Rank.KING)

        self.player.add_card_to_hand(card1)
        self.player.add_card_to_hand(card2)

        # Defensive player should defend with the lowest rank card first
        lowest_card = self.player.show_hand()[-1]  # Lowest rank in hand
        self.assertEqual(lowest_card, card1)


if __name__ == '__main__':
    unittest.main()
