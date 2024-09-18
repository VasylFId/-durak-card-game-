import logging
import unittest
from game_logic.players import Player
from game_logic.card_package import Card, Suit, Rank

# Setup logging before any tests
logger = logging.getLogger(__name__)


class TestPlayer(unittest.TestCase):
    def setUp(self):
        """
        Initialize a Player instance for each test.
        """
        self.player = Player("Alice")

    def test_player_initialization(self):
        """
        Test that the player is initialized with the correct name and an empty hand.
        """
        self.assertEqual(self.player.name, "Alice")
        self.assertEqual(len(self.player.hand), 0)

    def test_add_card_to_hand(self):
        """
        Test that cards are correctly added to the player's hand.
        """
        card = Card(Suit.HEARTS, Rank.ACE)
        self.player.add_card_to_hand(card)
        self.assertIn(card, self.player.hand)

    def test_remove_card_from_hand(self):
        """
        Test that cards are correctly removed from the player's hand.
        """
        card = Card(Suit.HEARTS, Rank.ACE)
        self.player.add_card_to_hand(card)
        removed = self.player.remove_card_from_hand(card)
        self.assertTrue(removed)
        self.assertNotIn(card, self.player.hand)

    def test_remove_nonexistent_card(self):
        """
        Test that removing a card not in the hand returns False.
        """
        card = Card(Suit.HEARTS, Rank.ACE)
        removed = self.player.remove_card_from_hand(card)
        self.assertFalse(removed)

    def test_sort_hand_without_trump(self):
        """
        Test that the player's hand is sorted correctly when there is no trump card.
        """
        cards = [
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.SIX),
            Card(Suit.CLUBS, Rank.TEN),
        ]
        for card in cards:
            self.player.add_card_to_hand(card)

        # Log the current trump suit before sorting
        current_trump_suit = self.player.trump_suit if hasattr(self.player, 'trump_suit') else None
        logger.info(f"Current trump suit before sorting (should be None): {current_trump_suit}")

        # No trump suit assigned, expect sorting by rank only
        expected_order = [
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.CLUBS, Rank.TEN),
            Card(Suit.HEARTS, Rank.SIX),
        ]
        self.assertEqual(self.player.show_hand(), expected_order)

    def test_sort_hand_with_trump(self):
        """
        Test that the player's hand is sorted correctly with trump cards first.
        """
        cards = [
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.HEARTS, Rank.SIX),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.ACE),
        ]
        for card in cards:
            self.player.add_card_to_hand(card)
        self.player.update_trump_suit(Suit.HEARTS)
        # Expect the hand to have trump cards (HEARTS) first, sorted by rank
        expected_order = [
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.HEARTS, Rank.SIX),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
        ]
        self.assertEqual(self.player.show_hand(), expected_order)

    def test_has_cards(self):
        """
        Test that the has_cards method accurately reflects whether the player
        has any cards left.
        """
        self.assertFalse(self.player.has_cards())
        card = Card(Suit.HEARTS, Rank.ACE)
        self.player.add_card_to_hand(card)
        self.assertTrue(self.player.has_cards())

    def test_empty_hand(self):
        """
        Test that the player's hand can be emptied properly.
        """
        card1 = Card(Suit.HEARTS, Rank.ACE)
        card2 = Card(Suit.SPADES, Rank.KING)
        self.player.add_card_to_hand(card1)
        self.player.add_card_to_hand(card2)
        self.player.remove_card_from_hand(card1)
        self.player.remove_card_from_hand(card2)
        self.assertEqual(len(self.player.hand), 0)

    def test_update_trump_suit(self):
        """
        Test that the trump suit can be updated and affects hand sorting.
        """
        card1 = Card(Suit.HEARTS, Rank.ACE)
        card2 = Card(Suit.SPADES, Rank.KING)
        card3 = Card(Suit.CLUBS, Rank.TEN)
        self.player.add_card_to_hand(card1)
        self.player.add_card_to_hand(card2)
        self.player.add_card_to_hand(card3)

        self.player.update_trump_suit(Suit.SPADES)

        # Expect the hand to have trump cards (SPADES) first, sorted by rank
        expected_order = [
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.CLUBS, Rank.TEN),
        ]
        self.assertEqual(self.player.show_hand(), expected_order)


if __name__ == "__main__":
    unittest.main()
