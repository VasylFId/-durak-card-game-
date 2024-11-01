"""
Unit tests for the InputManager class in the Durak game.

This module contains various tests to ensure that the InputManager class is
working as expected. It includes tests to check if the player can select a card
to attack, if the player can select a card to defend, and if the player can
select a card to defend when the board is full.
"""

import unittest
from unittest.mock import patch
from game_logic.players import Player
from game_logic.card_package import Card, Suit, Rank
from game_logic.game_management import BoardManager, PlayerManager
from game_logic.game_management import UserInputManager


class TestUserInputManager(unittest.TestCase):

    def setUp(self):
        """
        Initialize the UserInputManager, Player, and BoardManager instances
        for each test. Add some cards to the player's hand and set the trump
        card
        """

        self.user_input_manager = UserInputManager()
        self.player = Player(name="TestPlayer")

        # Add some cards to the player's hand
        self.cards_in_hand = [
            Card(Suit.DIAMONDS, Rank.KING),   # ♦️K
            Card(Suit.CLUBS, Rank.ACE),       # ♣️A
            Card(Suit.CLUBS, Rank.KING),      # ♣️K
            Card(Suit.HEARTS, Rank.KING),     # ♥️K
            Card(Suit.DIAMONDS, Rank.QUEEN),  # ♦️Q
            Card(Suit.CLUBS, Rank.QUEEN)      # ♣️Q
        ]

        for card in self.cards_in_hand:
            PlayerManager.add_card_to_hand(self.player, card)

        trump_card = Card(Suit.DIAMONDS, Rank.SEVEN)  # ♦️7
        PlayerManager.set_player_trump_suit(self.player, trump_card)

        # Sorted hand - [♦️A, ♦️Q, ♣️A, ♣️K, ♥️K, ♣️Q]

        self.board_manager = BoardManager(trump_card=trump_card)

    def test_get_card_from_player_attack(self):
        """
        Test case where the player selects a card to attack with.
        """

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['y']):
            selected_card = self.user_input_manager.get_card_from_player(
                self.board_manager, self.player, "attack")
            self.assertEqual(selected_card, Card(Suit.CLUBS, Rank.QUEEN))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)

        # Check that the card is no longer in the player's hand
        self.assertNotIn(selected_card,
                         PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_attack_with_board(self):
        """
        Test case where the player selects a card to attack with when the board
        is not empty.
        """

        # Number of cards in player's hand: 6
        number_of_cards_in_hand = len(PlayerManager.get_player_hand(
            self.player))

        # Add a card to the board (♥️10 and ♦️10)
        self.board_manager.add_card_to_board(Card(Suit.HEARTS, Rank.TEN))
        self.board_manager.add_card_to_board(Card(Suit.DIAMONDS, Rank.TEN))

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['y']):
            selected_card = self.user_input_manager.get_card_from_player(
                self.board_manager, self.player, "attack")
            self.assertEqual(selected_card, None)

        # Check that no card was removed from the player's hand
        self.assertEqual(len(PlayerManager.get_player_hand(self.player)),
                         number_of_cards_in_hand)

    def test_get_card_from_player_attack_decline_suggested(self):
        """
        Test case where the player declines the suggested card to attack with.
        """

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['n', '5']):
            selected_card = self.user_input_manager.get_card_from_player(
                self.board_manager, self.player, "attack")

            # Check that the player selected the card ♥️K
            self.assertEqual(selected_card, Card(Suit.HEARTS, Rank.KING))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card,
                         PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_defense(self):
        """
        Test case where the player selects a card to defend with.
        """

        # Add a card to the board
        attacking_card = Card(Suit.CLUBS, Rank.TEN) # ♣️10

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['y']):
            selected_card = self.user_input_manager.get_card_from_player(
                self.board_manager, self.player, "defense", attacking_card)
            self.assertEqual(selected_card, Card(Suit.CLUBS, Rank.QUEEN))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card,
                         PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_defense_trump_beat(self):
        """
        Test case where the player selects a card to defend with that beats the
        attacking card.
        """

        # Add a card to the board
        attacking_card = Card(Suit.SPADES, Rank.ACE)  # ♠️A

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['y']):
            selected_card = self.user_input_manager.get_card_from_player(
                self.board_manager, self.player, "defense", attacking_card)
            self.assertEqual(selected_card, Card(Suit.DIAMONDS, Rank.QUEEN))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card,
                         PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_defense_fail(self):
        """
        Test case where the player fails to defend against the attacking card.
        """

        # Number of cards in player's hand: 6
        number_of_cards_in_hand = len(PlayerManager.get_player_hand(
            self.player))

        # Add a card to the board
        attacking_card = Card(Suit.DIAMONDS, Rank.ACE)

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['fail', '6']):
            selected_card = self.user_input_manager.get_card_from_player(
                self.board_manager, self.player, "defense", attacking_card)
            self.assertEqual(selected_card, None)
            PlayerManager.add_card_to_hand(self.player, attacking_card)

        # Check that no card was removed from the player's hand
        self.assertNotEqual(len(PlayerManager.get_player_hand(self.player)),
                            number_of_cards_in_hand)

    def test_get_card_from_player_defense_decline_suggested(self):
        """
        Test case where the player declines the suggested card to defend with.
        """

        # Add a card to the board
        attacking_card = Card(Suit.CLUBS, Rank.TEN)  # ♣️10

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['n', '3']):
            selected_card = self.user_input_manager.get_card_from_player(
                self.board_manager, self.player, "defense", attacking_card)
            self.assertEqual(selected_card, Card(Suit.CLUBS, Rank.ACE))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card,
                         PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_invalid_input(self):
        """
        Test case where the player enters invalid input.
        """

        # Mock input to simulate user interaction with invalid input
        with patch('builtins.input', side_effect=['invalid', 'n', '6']):
            selected_card = self.user_input_manager.get_card_from_player(
                self.board_manager, self.player, "attack")
            self.assertEqual(selected_card, Card(Suit.CLUBS, Rank.QUEEN))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card,
                         PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_invalid_input_out_of_range(self):
        """
        Test case where the player enters invalid input that is out of range.
        """

        # Mock input to simulate user interaction with invalid input
        with patch('builtins.input', side_effect=['invalid', 'n', '-1', '6']):
            selected_card = self.user_input_manager.get_card_from_player(
                self.board_manager, self.player, "attack")
            self.assertEqual(selected_card, Card(Suit.CLUBS, Rank.QUEEN))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card,
                         PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_no_suitable_card_for_defense(self):
        """
        Test case where the player has no suitable card to defend with.
        """

        # Add a card to the board
        attacking_card = Card(Suit.SPADES, Rank.ACE)  # ♠️A

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['n', '4']):
            selected_card = self.user_input_manager.get_card_from_player(
                self.board_manager, self.player, "defense", attacking_card)
            self.assertEqual(selected_card, Card(Suit.CLUBS, Rank.KING))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card,
                         PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_empty_hand(self):
        """
        Test case where the player has no cards in hand.
        """

        # Create a player with an empty hand
        empty_player = Player(name="EmptyHandPlayer")

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['1']):
            with self.assertRaises(ValueError):
                self.user_input_manager.get_card_from_player(
                    self.board_manager, empty_player, "attack")


if __name__ == '__main__':
    unittest.main()
