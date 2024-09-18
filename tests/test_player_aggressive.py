import unittest
from game_logic.players import Player
from game_logic.card_package import Card, Suit, Rank
from utils.logger_setup import setup_logging

# Setup logging before any tests
setup_logging()


class TestPlayerAggressive(unittest.TestCase):
    def setUp(self):
        self.player = Player(name="Charlie")

    def test_aggressive_behavior(self):
        """
        Test that an aggressive player (Charlie) correctly adds cards to hand
        and sorts them with high cards first, respecting the trump suit.
        """
        card1 = Card(Suit.HEARTS, Rank.ACE)
        card2 = Card(Suit.SPADES, Rank.KING)
        card3 = Card(Suit.CLUBS, Rank.QUEEN)

        self.player.add_card_to_hand(card1)
        self.player.add_card_to_hand(card2)
        self.player.add_card_to_hand(card3)

        self.assertIn(card1, self.player.show_hand())
        self.assertIn(card2, self.player.show_hand())
        self.assertIn(card3, self.player.show_hand())

        # Sort hand with trump suit and ensure high cards are sorted first
        self.player.update_trump_suit(Suit.CLUBS)
        expected_order = [card3, card1, card2]
        self.assertEqual(self.player.show_hand(), expected_order)

    def test_attack_with_highest_card(self):
        """
        Test that an aggressive player (Charlie) attacks with the highest
        possible card first.
        """
        card1 = Card(Suit.HEARTS, Rank.SIX)
        card2 = Card(Suit.HEARTS, Rank.ACE)

        self.player.add_card_to_hand(card1)
        self.player.add_card_to_hand(card2)

        # Assume Charlie attacks with the highest possible card first
        attacking_card = self.player.show_hand()[0]  # Highest rank in hand
        self.assertEqual(attacking_card, card2)


if __name__ == '__main__':
    unittest.main()
