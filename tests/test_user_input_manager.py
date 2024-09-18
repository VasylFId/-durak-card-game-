import unittest
from unittest.mock import patch
from game_logic.players import Player
from game_logic.card_package import Card, Suit, Rank
from game_logic.game_management import UserInputManager, PlayerManager, BoardManager


class TestUserInputManager(unittest.TestCase):

    def setUp(self):
        self.user_input_manager = UserInputManager()
        self.player = Player(name="TestPlayer")

        # Add some cards to the player's hand
        self.cards_in_hand = [
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.QUEEN)
        ]

        for card in self.cards_in_hand:
            PlayerManager.add_card_to_hand(self.player, card)

        trump_card = Card(Suit.DIAMONDS, Rank.SEVEN)
        PlayerManager.set_player_trump_suit(self.player, trump_card)

        self.board_manager = BoardManager(trump_card=trump_card)

        # Sorted hand
        # [♦️A, ♦️Q, ♣️A, ♣️K, ♥️K, ♣️Q]

    def test_get_card_from_player_attack(self):
        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['y']):
            selected_card = self.user_input_manager.get_card_from_player(self.board_manager, self.player, "attack")
            self.assertEqual(selected_card, Card(Suit.CLUBS, Rank.QUEEN))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card, PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_attack_with_board(self):
        # Number of cards in player's hand: 6
        number_of_cards_in_hand = len(PlayerManager.get_player_hand(self.player))

        # Add a card to the board
        self.board_manager.add_card_to_board(Card(Suit.HEARTS, Rank.TEN))
        self.board_manager.add_card_to_board(Card(Suit.DIAMONDS, Rank.TEN))

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['y']):
            selected_card = self.user_input_manager.get_card_from_player(self.board_manager, self.player, "attack")
            self.assertEqual(selected_card, None)

        # Check that no card was removed from the player's hand
        self.assertEqual(len(PlayerManager.get_player_hand(self.player)), number_of_cards_in_hand)
    

    def test_get_card_from_player_attack_decline_suggested(self):
        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['n', '5']):
            selected_card = self.user_input_manager.get_card_from_player(self.board_manager, self.player, "attack")
            self.assertEqual(selected_card, Card(Suit.HEARTS, Rank.KING))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card, PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_defense(self):
        attacking_card = Card(Suit.CLUBS, Rank.TEN)

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['y']):
            selected_card = self.user_input_manager.get_card_from_player(self.board_manager, self.player, "defense", attacking_card)
            self.assertEqual(selected_card, Card(Suit.CLUBS, Rank.QUEEN))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card, PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_defense_trump_beat(self):
        attacking_card = Card(Suit.SPADES, Rank.ACE)

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['y']):
            selected_card = self.user_input_manager.get_card_from_player(self.board_manager, self.player, "defense", attacking_card)
            self.assertEqual(selected_card, Card(Suit.DIAMONDS, Rank.QUEEN))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card, PlayerManager.get_player_hand(self.player))
        
    def test_get_card_from_player_defense_fail(self):
        # Number of cards in player's hand: 6
        number_of_cards_in_hand = len(PlayerManager.get_player_hand(self.player))

        # Add a card to the board
        attacking_card = Card(Suit.DIAMONDS, Rank.ACE)

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['fail', '6']):
            selected_card = self.user_input_manager.get_card_from_player(self.board_manager, self.player, "defense", attacking_card)
            self.assertEqual(selected_card, None)
            PlayerManager.add_card_to_hand(self.player, attacking_card)

        # Check that no card was removed from the player's hand
        self.assertNotEqual(len(PlayerManager.get_player_hand(self.player)), number_of_cards_in_hand)

        




    def test_get_card_from_player_defense_decline_suggested(self):
        attacking_card = Card(Suit.CLUBS, Rank.TEN)

        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['n', '3']):
            selected_card = self.user_input_manager.get_card_from_player(self.board_manager, self.player, "defense", attacking_card)
            self.assertEqual(selected_card, Card(Suit.CLUBS, Rank.ACE))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card, PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_invalid_input(self):
        # Mock input to simulate user interaction with invalid input
        with patch('builtins.input', side_effect=['invalid', 'n', '6']):
            selected_card = self.user_input_manager.get_card_from_player(self.board_manager, self.player, "attack")
            self.assertEqual(selected_card, Card(Suit.CLUBS, Rank.QUEEN))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card, PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_invalid_input_out_of_range(self):
        # Mock input to simulate user interaction with invalid input
        with patch('builtins.input', side_effect=['invalid', 'n', '-1', '6']):
            selected_card = self.user_input_manager.get_card_from_player(self.board_manager, self.player, "attack")
            self.assertEqual(selected_card, Card(Suit.CLUBS, Rank.QUEEN))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card, PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_no_suitable_card_for_defense(self):
        attacking_card = Card(Suit.SPADES, Rank.ACE)
        
        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['n', '4']):
            selected_card = self.user_input_manager.get_card_from_player(self.board_manager, self.player, "defense", attacking_card)
            self.assertEqual(selected_card, Card(Suit.CLUBS, Rank.KING))

        # Check that the card was removed from the player's hand
        PlayerManager.remove_card_from_hand(self.player, selected_card)
        self.assertNotIn(selected_card, PlayerManager.get_player_hand(self.player))

    def test_get_card_from_player_empty_hand(self):
        empty_player = Player(name="EmptyHandPlayer")
        
        # Mock input to simulate user interaction
        with patch('builtins.input', side_effect=['1']):
            with self.assertRaises(ValueError):
                self.user_input_manager.get_card_from_player(self.board_manager, empty_player, "attack")


if __name__ == '__main__':
    unittest.main()