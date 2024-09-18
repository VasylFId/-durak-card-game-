import logging
import unittest
from game_logic.card_package import Deck, Card, Suit, Rank
from game_logic.players import Player
from game_logic.game_management import PlayerManager, DeckManager

logger = logging.getLogger(__name__)


class TestPlayerManager(unittest.TestCase):

    def setUp(self):
        """
        Set up a new deck and player before each test.
        """
        self.deck = Deck()
        self.player = Player(name="TestPlayer")

    def test_player_has_enough_cards(self):
        """
        Test if player_has_enough_cards correctly identifies when a player
        has the minimum number of cards.
        """
        # Initially, the player has no cards
        self.assertFalse(PlayerManager.player_has_enough_cards(self.player))

        # Give the player 6 cards
        for _ in range(6):
            self.player.hand.append(DeckManager.draw_card(self.deck))

        self.assertTrue(PlayerManager.player_has_enough_cards(self.player))

    def test_deal_initial_cards(self):
        """
        Test if deal_initial_cards gives the player the correct number of cards.
        """
        # Initially, the player has no cards
        self.assertEqual(len(self.player.hand), 0)

        # Deal initial cards
        PlayerManager.deal_initial_cards(self.deck, self.player, hand_size=6)

        # Check if the player has 6 cards after dealing
        self.assertEqual(len(self.player.hand), 6)

    def test_add_card_to_hand(self):
        """
        Test if add_card_to_hand correctly adds a card to the player's hand.
        """
        # Draw a card from the deck
        card_to_add = DeckManager.draw_card(self.deck)

        # Add card to player's hand
        PlayerManager.add_card_to_hand(self.player, card_to_add)

        # Check if the card is now in the player's hand
        self.assertIn(card_to_add, self.player.hand)
        self.assertEqual(len(self.player.hand), 1)

    def test_set_player_mock_trump_suit(self):
        """
        Test setting the player's trump suit.
        """
        trump_card = Card(Suit.HEARTS, Rank.ACE)
        PlayerManager.set_player_trump_suit(self.player, trump_card)
        self.assertEqual(self.player.trump_suit, Suit.HEARTS)

    def test_set_player_trump_suit_from_deck(self):
        """
        Test setting the player's trump suit from the deck.
        """
        # Draw a card from the deck
        trump_card = DeckManager.get_trump_card(self.deck)

        # Set the trump suit from the card
        PlayerManager.set_player_trump_suit(self.player, trump_card)

        # Check if the trump suit is set correctly
        self.assertEqual(self.player.trump_suit, trump_card.suit)

    def test_get_player_trump_suit(self):
        """
        Test getting the player's trump suit.
        """
        self.player.trump_suit = Suit.CLUBS
        suit = PlayerManager.get_player_trump_suit(self.player)
        self.assertEqual(suit, Suit.CLUBS)

    def test_get_player_hand(self):
        """
        Test getting the player's hand.
        """
        expected_hand = [
            Card(Suit.CLUBS, Rank.KING), # ♣️K 
            Card(Suit.HEARTS, Rank.SEVEN) # ♥️7
        ]

        # Set the player's hand
        for card in expected_hand:
            PlayerManager.add_card_to_hand(self.player, card)

        trump_card = DeckManager.get_trump_card(self.deck)

        # Set the player's trump suit
        PlayerManager.set_player_trump_suit(self.player, trump_card)

        hand = PlayerManager.get_player_hand(self.player)
        player_trump_suit = PlayerManager.get_player_trump_suit(self.player)

        # Log the player's trump suit
        logger.info(f"{self.player.name}'s trump suit is {player_trump_suit = }")

        # Check if the hand is sorted correctly
        if player_trump_suit == Suit.HEARTS:
            logger.info("Trump suit is Hearts")
            logger.info("Expected hand: " + str(expected_hand))
            expected_hand[0], expected_hand[-1] = expected_hand[-1], expected_hand[0]
            logger.info("Reversed expected hand: " + str(expected_hand))

        self.assertEqual(hand, expected_hand)

    def test_remove_card_from_hand(self):
        """
        Test if remove_card_from_hand correctly removes a card from the player's hand.
        """
        # Add a card to the player's hand
        card_to_remove = Card(Suit.CLUBS, Rank.KING)
        PlayerManager.add_card_to_hand(self.player, card_to_remove)

        # Remove the card from the player's hand
        PlayerManager.remove_card_from_hand(self.player, card_to_remove)

        # Check if the card is no longer in the player's hand
        self.assertNotIn(card_to_remove, self.player.hand)
        self.assertEqual(len(self.player.hand), 0)

        # Test removing a card that is not in the hand
        with self.assertRaises(ValueError):
            PlayerManager.remove_card_from_hand(self.player, card_to_remove)

    def test_pick_up_card(self):
        """
        Test if pick_up_card correctly adds a card to the player's hand.
        """
        # Create a card to pick up
        card_to_pick_up = Card(Suit.HEARTS, Rank.ACE)

        # Pick up the card
        PlayerManager.pick_up_card(self.player, card_to_pick_up)

        # Check if the card is now in the player's hand
        self.assertIn(card_to_pick_up, self.player.hand)
        self.assertEqual(len(self.player.hand), 1)

    def test_select_card(self):
        """
        Test if select_card correctly selects a card from the player's hand.
        """
        # Add a card to the player's hand
        card_to_select = Card(Suit.DIAMONDS, Rank.QUEEN)
        PlayerManager.add_card_to_hand(self.player, card_to_select)

        # Select the card
        selected_card = PlayerManager.select_card(self.player, card_to_select)

        # Check if the selected card is the one we expected
        self.assertEqual(selected_card, card_to_select)

        # Test selecting a card that is not in the hand
        with self.assertRaises(ValueError):
            PlayerManager.select_card(self.player, Card(Suit.SPADES, Rank.TEN))

    def test_add_and_remove_multiple_cards(self):
        """
        Test adding multiple cards to a player's hand and then removing them.
        """
        # Add multiple cards to the player's hand
        cards_to_add = [
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.SPADES, Rank.TEN),
            Card(Suit.CLUBS, Rank.ACE)
        ]

        for card in cards_to_add:
            PlayerManager.add_card_to_hand(self.player, card)

        # Verify that all cards were added
        for card in cards_to_add:
            self.assertIn(card, self.player.hand)

        # Remove each card and verify removal
        for card in cards_to_add:
            PlayerManager.remove_card_from_hand(self.player, card)
            self.assertNotIn(card, self.player.hand)

        # Check that the player's hand is empty after removing all cards
        self.assertEqual(len(self.player.hand), 0)

    def test_pick_up_and_select_card(self):
        """
        Test picking up a card and then selecting it.
        """
        # Pick up a card
        card_to_pick_up = Card(Suit.DIAMONDS, Rank.QUEEN)
        PlayerManager.pick_up_card(self.player, card_to_pick_up)

        # Verify that the card is in the player's hand
        self.assertIn(card_to_pick_up, self.player.hand)

        # Select the card
        selected_card = PlayerManager.select_card(self.player, card_to_pick_up)

        # Verify that the selected card is the one we picked up
        self.assertEqual(selected_card, card_to_pick_up)

    def test_add_pick_up_and_remove_cards(self):
        """
        Test adding, picking up, and then removing cards from a player's hand.
        """
        # Add a card to the player's hand
        card1 = Card(Suit.HEARTS, Rank.KING)
        PlayerManager.add_card_to_hand(self.player, card1)

        # Pick up another card
        card2 = Card(Suit.SPADES, Rank.TEN)
        PlayerManager.pick_up_card(self.player, card2)

        # Verify both cards are in the player's hand
        self.assertIn(card1, self.player.hand)
        self.assertIn(card2, self.player.hand)

        # Remove both cards
        PlayerManager.remove_card_from_hand(self.player, card1)
        PlayerManager.remove_card_from_hand(self.player, card2)

        # Verify that the player's hand is empty after removing all cards
        self.assertEqual(len(self.player.hand), 0)


if __name__ == '__main__':
    unittest.main()
