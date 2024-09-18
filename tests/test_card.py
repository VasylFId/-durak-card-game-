"""
Unit tests for the Card class in the Durak card game.

This module contains various tests to ensure that the Card class
in the card_package module behaves as expected. It includes tests
for creating cards, determining trump cards, comparing cards of
different suits and ranks, and checking for card equality.

"""

import unittest
from utils.logger_setup import setup_logging
from game_logic.card_package import Card, Suit, Rank

# Call setup_logging before any logging
setup_logging()


class TestCard(unittest.TestCase):

    """
    A class containing unit tests for the Card class.
    """

    def test_card_creation(self):
        """Tests the creation of a card and verifies its attributes."""
        card = Card(Suit.HEARTS, Rank.ACE)
        self.assertEqual(card.suit, Suit.HEARTS)
        self.assertEqual(card.rank, Rank.ACE)
        self.assertEqual(card.weight, 14)

    def test_is_trump(self):
        """Tests if a card is correctly identified as a trump card."""
        card = Card(Suit.HEARTS, Rank.ACE)
        self.assertTrue(card.is_trump(Suit.HEARTS))
        self.assertFalse(card.is_trump(Suit.CLUBS))

    def test_compare_trump_vs_non_trump(self):
        """
        Tests the comparison between a trump card and a
        non-trump card.
        """
        trump_card = Card(Suit.HEARTS, Rank.SIX)
        non_trump_card = Card(Suit.CLUBS, Rank.ACE)
        self.assertEqual(trump_card.compare(non_trump_card,
                                            Suit.HEARTS), 1)
        self.assertEqual(non_trump_card.compare(trump_card,
                                                Suit.HEARTS), -1)

    def test_compare_same_suit(self):
        """
        Tests the comparison of two cards with the same suit
        but different ranks.
        """
        card1 = Card(Suit.HEARTS, Rank.SIX)
        card2 = Card(Suit.HEARTS, Rank.ACE)
        self.assertEqual(card1.compare(card2, Suit.CLUBS), -8)
        self.assertEqual(card2.compare(card1, Suit.CLUBS), 8)

    def test_compare_different_suits_non_trump(self):
        """
        Tests the comparison of two cards with different suits
        and neither being a trump card.
        """
        card1 = Card(Suit.HEARTS, Rank.SIX)
        card2 = Card(Suit.CLUBS, Rank.ACE)
        self.assertEqual(card1.compare(card2, Suit.SPADES), 0)

    def test_card_equality(self):
        """
        Tests the equality operator for two cards with the
        same suit and rank.
        """
        card1 = Card(Suit.HEARTS, Rank.ACE)
        card2 = Card(Suit.HEARTS, Rank.ACE)
        self.assertEqual(card1, card2)

    def test_card_inequality(self):
        """
        Tests the inequality operator for two cards with
        different suits or ranks.
        """
        card1 = Card(Suit.HEARTS, Rank.ACE)
        card2 = Card(Suit.CLUBS, Rank.ACE)
        card3 = Card(Suit.HEARTS, Rank.KING)
        self.assertNotEqual(card1, card2)
        self.assertNotEqual(card1, card3)

    def test_trump_beats_higher_non_trump(self):
        """
        Tests if a lower-ranked trump card beats a
        higher-ranked non-trump card.
        """
        trump_card = Card(Suit.HEARTS, Rank.SIX)
        higher_non_trump_card = Card(Suit.CLUBS, Rank.KING)
        self.assertEqual(trump_card.compare(higher_non_trump_card,
                                            Suit.HEARTS), 1)

    def test_same_rank_different_suits(self):
        """
        Tests the comparison of two cards with the same rank
        but different suits, when one is a trump card.
        """
        trump_card = Card(Suit.HEARTS, Rank.KING)
        non_trump_card = Card(Suit.CLUBS, Rank.KING)
        self.assertEqual(trump_card.compare(non_trump_card,
                                            Suit.HEARTS), 1)
        self.assertEqual(non_trump_card.compare(trump_card,
                                                Suit.HEARTS), -1)

    def test_different_ranks_different_suits(self):
        """
        Tests if cards with different ranks and suits are
        considered equal when neither is a trump card.
        """
        card1 = Card(Suit.HEARTS, Rank.SIX)
        card2 = Card(Suit.CLUBS, Rank.ACE)
        self.assertEqual(card1.compare(card2, Suit.DIAMONDS), 0)


if __name__ == '__main__':
    unittest.main()
