import unittest
from game_logic.card_package import Card, Suit, Rank
from game_logic.game_management import BoardManager


class TestBoardManager(unittest.TestCase):

    def setUp(self):
        self.trump_card = Card(Suit.HEARTS, Rank.ACE)
        self.board_manager = BoardManager(trump_card=self.trump_card)

    def test_add_card_to_board(self):
        card = Card(Suit.SPADES, Rank.TEN)
        self.board_manager.add_card_to_board(card)
        self.assertIn(card, self.board_manager.get_board_state())

    def test_get_board_state(self):
        card1 = Card(Suit.SPADES, Rank.TEN)
        card2 = Card(Suit.CLUBS, Rank.KING)
        self.board_manager.add_card_to_board(card1)
        self.board_manager.add_card_to_board(card2)
        self.assertEqual(self.board_manager.get_board_state(), [card1, card2])

    def test_get_board_ranks(self):
        card1 = Card(Suit.SPADES, Rank.TEN)
        card2 = Card(Suit.CLUBS, Rank.KING)
        self.board_manager.add_card_to_board(card1)
        self.board_manager.add_card_to_board(card2)
        self.assertEqual(self.board_manager.get_board_ranks(), {Rank.TEN, Rank.KING})

    def test_clear_board(self):
        card = Card(Suit.SPADES, Rank.TEN)
        self.board_manager.add_card_to_board(card)
        self.board_manager.clear_board()
        self.assertEqual(self.board_manager.get_board_state(), [])

    def test_is_board_full_first_round(self):
        for _ in range(10):
            self.board_manager.add_card_to_board(Card(Suit.SPADES, Rank.TEN))
        self.assertTrue(self.board_manager.is_board_full())

    def test_is_board_full_subsequent_rounds(self):
        self.board_manager.next_round()  # Move to round 2
        for _ in range(12):
            self.board_manager.add_card_to_board(Card(Suit.SPADES, Rank.TEN))
        self.assertTrue(self.board_manager.is_board_full())

    def test_next_round(self):
        card = Card(Suit.SPADES, Rank.TEN)
        self.board_manager.add_card_to_board(card)
        self.board_manager.next_round()
        self.assertEqual(self.board_manager.get_board_state(), [])
        self.assertEqual(self.board_manager.round_number, 2)


if __name__ == '__main__':
    unittest.main()
