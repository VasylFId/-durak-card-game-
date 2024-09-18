import unittest
from game_logic.card_package import Card, Suit, Rank
from game_logic.players import Player
from game_logic.game_management import BoardManager, RulesManager


class TestRulesManager(unittest.TestCase):

    def setUp(self):
        self.trump_card = Card(Suit.HEARTS, Rank.ACE)
        self.board_manager = BoardManager(trump_card=self.trump_card)
        self.attacker = Player(name="Attacker")
        self.defender = Player(name="Defender")

    def test_is_valid_attack_empty_board(self):
        card = Card(Suit.SPADES, Rank.TEN)
        self.assertTrue(RulesManager.is_valid_attack(self.board_manager, card))

    def test_is_valid_attack_matching_rank(self):
        card1 = Card(Suit.SPADES, Rank.TEN)
        card2 = Card(Suit.CLUBS, Rank.TEN)
        self.board_manager.add_card_to_board(card1)
        self.assertTrue(RulesManager.is_valid_attack(self.board_manager, card2))

    def test_is_valid_attack_non_matching_rank(self):
        card1 = Card(Suit.SPADES, Rank.TEN)
        card2 = Card(Suit.CLUBS, Rank.NINE)
        card3 = Card(Suit.CLUBS, Rank.KING)
        self.board_manager.add_card_to_board(card1)
        self.board_manager.add_card_to_board(card2)
        self.assertFalse(RulesManager.is_valid_attack(self.board_manager, card3))

    def test_is_valid_defense_valid(self):
        attack_card = Card(Suit.SPADES, Rank.TEN)
        defense_card = Card(Suit.SPADES, Rank.JACK)
        self.assertTrue(RulesManager.is_valid_defense(self.board_manager, attack_card, defense_card))

    def test_is_valid_defense_invalid(self):
        attack_card = Card(Suit.SPADES, Rank.TEN)
        defense_card = Card(Suit.SPADES, Rank.NINE)
        self.assertFalse(RulesManager.is_valid_defense(self.board_manager, attack_card, defense_card))

    def test_is_valid_defense_trump_ace_invalid(self):
        attack_card = Card(Suit.HEARTS, Rank.ACE)
        defense_card = Card(Suit.SPADES, Rank.TEN)
        self.assertFalse(RulesManager.is_valid_defense(self.board_manager, attack_card, defense_card))

    def test_is_valid_defense_trump_card(self):
        attack_card = Card(Suit.SPADES, Rank.TEN)
        defense_card = Card(Suit.HEARTS, Rank.SIX)  # Trump card
        self.assertTrue(RulesManager.is_valid_defense(self.board_manager, attack_card, defense_card))

    def test_is_board_full_first_round(self):
        for _ in range(10):
            self.board_manager.add_card_to_board(Card(Suit.SPADES, Rank.TEN))
        self.assertTrue(RulesManager.is_board_full(self.board_manager))

    def test_is_board_full_subsequent_rounds(self):
        self.board_manager.next_round()  # Move to round 2
        for _ in range(12):
            self.board_manager.add_card_to_board(Card(Suit.SPADES, Rank.TEN))
        self.assertTrue(RulesManager.is_board_full(self.board_manager))

    def test_full_hands_no_pickup(self):
        """
        Test case where both players have full hands (6 cards each), so no cards should be picked up.
        """
        self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),
                              Card(Suit.SPADES, Rank.NINE),
                              Card(Suit.SPADES, Rank.EIGHT),
                              Card(Suit.SPADES, Rank.SEVEN),
                              Card(Suit.SPADES, Rank.SIX),
                              Card(Suit.SPADES, Rank.KING)]
        self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),
                              Card(Suit.CLUBS, Rank.NINE),
                              Card(Suit.CLUBS, Rank.EIGHT),
                              Card(Suit.CLUBS, Rank.SEVEN),
                              Card(Suit.CLUBS, Rank.SIX),
                              Card(Suit.CLUBS, Rank.KING)]
        deck_size = 10

        result = RulesManager.determine_card_distribution(deck_size, self.attacker, self.defender)
        self.assertEqual(result, {"attacker": 0, "defender": 0})

    def test_attacker_needs_cards(self):
        """
        Test case where only the attacker needs cards, and the deck has enough cards.
        """
        self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),
                              Card(Suit.SPADES, Rank.NINE),
                              Card(Suit.SPADES, Rank.EIGHT),
                              Card(Suit.SPADES, Rank.SEVEN)]
        self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),
                              Card(Suit.CLUBS, Rank.NINE),
                              Card(Suit.CLUBS, Rank.EIGHT),
                              Card(Suit.CLUBS, Rank.SEVEN),
                              Card(Suit.CLUBS, Rank.SIX),
                              Card(Suit.CLUBS, Rank.KING)]
        deck_size = 10

        result = RulesManager.determine_card_distribution(deck_size, self.attacker, self.defender)
        self.assertEqual(result, {"attacker": 2, "defender": 0})

    def test_defender_needs_cards(self):
        """
        Test case where only the defender needs cards, and the deck has enough cards.
        """
        self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),
                              Card(Suit.SPADES, Rank.NINE),
                              Card(Suit.SPADES, Rank.EIGHT),
                              Card(Suit.SPADES, Rank.SEVEN),
                              Card(Suit.SPADES, Rank.SIX),
                              Card(Suit.SPADES, Rank.KING)]
        self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),
                              Card(Suit.CLUBS, Rank.NINE)]

        deck_size = 10

        result = RulesManager.determine_card_distribution(deck_size, self.attacker, self.defender)
        self.assertEqual(result, {"attacker": 0, "defender": 4})

    def test_both_need_cards_enough_in_deck(self):
        """
        Test case where both players need cards, and the deck has enough cards for both.
        """
        self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),
                              Card(Suit.SPADES, Rank.NINE),
                              Card(Suit.SPADES, Rank.EIGHT)]
        self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),
                              Card(Suit.CLUBS, Rank.NINE),
                              Card(Suit.CLUBS, Rank.SEVEN)]
        deck_size = 6  # Enough to give 3 to attacker and 3 to defender

        result = RulesManager.determine_card_distribution(deck_size, self.attacker, self.defender)
        self.assertEqual(result, {"attacker": 3, "defender": 3})

    def test_both_need_cards_not_enough_in_deck(self):
        """
        Test case where both players need cards, but the deck does not have enough cards.
        """
        self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),
                              Card(Suit.SPADES, Rank.NINE),
                              Card(Suit.SPADES, Rank.EIGHT),
                              Card(Suit.SPADES, Rank.SEVEN)]
        self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),
                              Card(Suit.CLUBS, Rank.NINE)]
        deck_size = 4  # Not enough cards to satisfy both players

        result = RulesManager.determine_card_distribution(deck_size, self.attacker, self.defender)
        # Attacker needs 2 cards, defender needs 4 cards, attacker gets 2, defender gets 2
        self.assertEqual(result, {"attacker": 2, "defender": 2})

    def test_both_need_cards_exact_amount_in_deck(self):
        """
        Test case where both players need cards, and the deck has the exact amount needed.
        """
        self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),
                              Card(Suit.SPADES, Rank.NINE)]
        self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),
                              Card(Suit.CLUBS, Rank.NINE),
                              Card(Suit.CLUBS, Rank.EIGHT),
                              Card(Suit.CLUBS, Rank.SEVEN)]
        deck_size = 6  # Just enough cards to split

        result = RulesManager.determine_card_distribution(deck_size, self.attacker, self.defender)
        self.assertEqual(result, {"attacker": 4, "defender": 2})

    def test_attacker_needs_cards_but_deck_empty(self):
        """
        Test case where the attacker needs cards, but the deck is empty.
        """
        self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),
                              Card(Suit.SPADES, Rank.NINE),
                              Card(Suit.SPADES, Rank.EIGHT),
                              Card(Suit.SPADES, Rank.SEVEN)]
        self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),
                              Card(Suit.CLUBS, Rank.NINE),
                              Card(Suit.CLUBS, Rank.EIGHT),
                              Card(Suit.CLUBS, Rank.SEVEN),
                              Card(Suit.CLUBS, Rank.SIX),
                              Card(Suit.CLUBS, Rank.KING)]

        deck_size = 0  # Empty deck

        result = RulesManager.determine_card_distribution(deck_size, self.attacker, self.defender)
        self.assertEqual(result, {"attacker": 0, "defender": 0})

    def test_both_players_need_cards_deck_nearly_empty(self):
        """
        Test case where both players need cards, but the deck has very few cards left.
        """
        self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),
                              Card(Suit.SPADES, Rank.NINE)]
        self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),
                              Card(Suit.CLUBS, Rank.NINE)]

        deck_size = 2  # Only 1 card left in the deck for each player

        result = RulesManager.determine_card_distribution(deck_size, self.attacker, self.defender)
        # In this case, one player will get the only card left
        self.assertEqual(result, {"attacker": 1, "defender": 1})

    def test_both_players_have_more_than_six_cards(self):
        """
        Test case where both players have more than 6 cards and don't need to pick up any cards.
        """
        self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),
                              Card(Suit.SPADES, Rank.NINE),
                              Card(Suit.SPADES, Rank.EIGHT),
                              Card(Suit.SPADES, Rank.SEVEN),
                              Card(Suit.SPADES, Rank.SIX),
                              Card(Suit.SPADES, Rank.KING),
                              Card(Suit.SPADES, Rank.QUEEN)]
        self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),
                              Card(Suit.CLUBS, Rank.NINE),
                              Card(Suit.CLUBS, Rank.EIGHT),
                              Card(Suit.CLUBS, Rank.SEVEN),
                              Card(Suit.CLUBS, Rank.SIX),
                              Card(Suit.CLUBS, Rank.KING),
                              Card(Suit.CLUBS, Rank.QUEEN)]

        deck_size = 10

        result = RulesManager.determine_card_distribution(deck_size, self.attacker, self.defender)
        self.assertEqual(result, {"attacker": 0, "defender": 0})


if __name__ == '__main__':
    unittest.main()