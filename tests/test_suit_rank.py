"""
Unit tests for the Suit and Rank enumerations in the Durak card game.

This module contains tests to ensure that the Suit and Rank
enumerations in the card_package module behave as expected. It
includes tests for string representation and natural ordering
of ranks.
"""

import unittest
from game_logic.card_package import Suit, Rank


class TestSuitRank(unittest.TestCase):

    """
    A class containing unit tests for the Suit and Rank enumerations.
    """

    def test_suit_enum(self):
        """
        Tests the string representation of each Suit enumeration
        value.
        """
        self.assertEqual(str(Suit.HEARTS), "♥️")
        self.assertEqual(str(Suit.DIAMONDS), "♦️")
        self.assertEqual(str(Suit.CLUBS), "♣️")
        self.assertEqual(str(Suit.SPADES), "♠️")

    def test_rank_enum(self):
        """
        Tests the string representation of each Rank enumeration
        value.
        """
        self.assertEqual(str(Rank.SIX), "6")
        self.assertEqual(str(Rank.SEVEN), "7")
        self.assertEqual(str(Rank.EIGHT), "8")
        self.assertEqual(str(Rank.NINE), "9")
        self.assertEqual(str(Rank.TEN), "10")
        self.assertEqual(str(Rank.JACK), "J")
        self.assertEqual(str(Rank.QUEEN), "Q")
        self.assertEqual(str(Rank.KING), "K")
        self.assertEqual(str(Rank.ACE), "A")

    def test_rank_comparison(self):
        """
        Tests the natural ordering of ranks to ensure that the
        comparison operators work as expected.
        """
        self.assertTrue(Rank.SIX < Rank.SEVEN)
        self.assertTrue(Rank.JACK > Rank.TEN)
        self.assertTrue(Rank.ACE > Rank.KING)


if __name__ == '__main__':
    unittest.main()
