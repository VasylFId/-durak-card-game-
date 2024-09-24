import unittest
from game_logic.card_package import Card, Deck, Suit, Rank
from game_logic.players import Player
from game_logic.game_management import RoundManager, PlayerManager, TurnManager


class TestRoundManager(unittest.TestCase):

    def setUp(self):
        """
        Set up the RoundManager with a deck and two players for testing.
        """
        # Set up deck and players
        self.deck = Deck()
        self.attacker = Player(name="Alice")
        self.defender = Player(name="Bob")
        self.players = [self.attacker, self.defender]

        # Set up the RoundManager
        self.round_manager = RoundManager(self.deck, self.players)

        # Set up initial cards for each player
        attacker_cards = [
            Card(Suit.CLUBS, Rank.SIX),
            Card(Suit.CLUBS, Rank.TEN),
            Card(Suit.DIAMONDS, Rank.SEVEN),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.EIGHT),
            Card(Suit.HEARTS, Rank.JACK)
        ]

        defender_cards = [
            Card(Suit.DIAMONDS, Rank.SIX),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.EIGHT),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.HEARTS, Rank.SEVEN),
            Card(Suit.HEARTS, Rank.TEN)
        ]

        for card in attacker_cards:
            PlayerManager.add_card_to_hand(self.attacker, card)

        for card in defender_cards:
            PlayerManager.add_card_to_hand(self.defender, card)

    def test_start_round(self):
        """
        Test the start_round method of the RoundManager.
        """
        self.round_manager.start_round()

        self.assertEqual(self.round_manager.current_attacker, self.attacker)
        self.assertEqual(self.round_manager.current_defender, self.defender)
        self.assertIsInstance(self.round_manager.turn_manager, TurnManager)

        # Ensure both players have 6 cards at the start
        self.assertEqual(len(PlayerManager.get_player_hand(self.attacker)), 6)
        self.assertEqual(len(PlayerManager.get_player_hand(self.defender)), 6)

    def test_process_attack(self):
        """
        Test the process_attack method of the RoundManager.
        """
        self.round_manager.start_round()

        # Attacker plays a card to attack
        attack_card = PlayerManager.get_player_hand(self.attacker)[-1]
        result = self.round_manager.process_attack(attack_card)

        self.assertTrue(result)
        self.assertEqual(self.round_manager.turn_manager.turn_state["attacks"], [attack_card])
        self.assertEqual(self.round_manager.turn_manager.is_attacker_turn, False)
        self.assertEqual(self.round_manager.turn_manager.is_defender_turn, True)

    def test_process_defense(self):
        """
        Test the process_defense method of the RoundManager.
        """
        self.round_manager.start_round()

        # Attacker plays a card to attack
        attack_card = PlayerManager.get_player_hand(self.attacker)[-1]
        self.round_manager.process_attack(attack_card)

        # Defender plays a card to defend
        defense_card = PlayerManager.get_player_hand(self.defender)[-2]
        result = self.round_manager.process_defense(defense_card, attack_card)

        self.assertTrue(result)
        self.assertEqual(self.round_manager.turn_manager.turn_state["defenses"], [defense_card])
        self.assertEqual(self.round_manager.turn_manager.is_attacker_turn, True)
        self.assertEqual(self.round_manager.turn_manager.is_defender_turn, False)

    def test_prepare_for_next_round(self):
        """
        Test the prepare_for_next_round method of the RoundManager.
        """
        self.round_manager.start_round()

        # Simulate the end of the round
        self.round_manager.prepare_for_next_round()

        # Ensure the round number increased
        self.assertEqual(self.round_manager.round_number, 2)

        # Ensure attacker and defender switched
        self.assertEqual(self.round_manager.current_attacker, self.defender)
        self.assertEqual(self.round_manager.current_defender, self.attacker)

    def test_is_round_over(self):
        """
        Test the is_round_over method of the RoundManager.
        """
        self.round_manager.start_round()

        # Add cards to the board to fill it up
        for _ in range(10):  # Maximum number of cards for round 1 is 10
            self.round_manager.turn_manager.board_manager.add_card_to_board(Card(Suit.HEARTS, Rank.SIX))

        # Check if the round is over
        self.assertTrue(self.round_manager.is_round_over())

    def test_check_game_over(self):
        """
        Test the check_game_over method of the RoundManager.
        """
        self.round_manager.start_round()

        # Simulate the game-over condition: a player has no cards left
        for _ in range(6):
            PlayerManager.remove_card_from_hand(self.attacker, PlayerManager.get_player_hand(self.attacker)[0])

        self.assertTrue(self.round_manager.check_game_over())

    def test_check_game_not_over(self):
        """
        Test that the game is not over if players still have cards.
        """
        self.round_manager.start_round()
        self.assertFalse(self.round_manager.check_game_over())

    def test_deal_cards(self):
        """
        Test that players are dealt cards correctly if they have fewer than 6 cards.
        """
        # Remove cards from players' hands to simulate needing more cards
        PlayerManager.remove_card_from_hand(self.attacker, PlayerManager.get_player_hand(self.attacker)[0])
        PlayerManager.remove_card_from_hand(self.defender, PlayerManager.get_player_hand(self.defender)[0])

        # Start the round, which should deal cards to bring players back to 6 cards
        self.round_manager.start_round()

        self.assertEqual(len(PlayerManager.get_player_hand(self.attacker)), 6)
        self.assertEqual(len(PlayerManager.get_player_hand(self.defender)), 6)


if __name__ == '__main__':
    unittest.main()
