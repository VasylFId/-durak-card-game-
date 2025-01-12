# """
# Unit tests for the BoardManager class in the Durak card game.

# This module contains various tests to ensure that the BoardManager class
# in the game_management module behaves as expected. It includes tests for
# adding cards to the board, getting the board state, getting the board ranks,
# clearing the board, checking if the board is full, and moving to the next round
# """


# import unittest
# from game_logic.card_package import Card, Suit, Rank
# from game_logic.game_management import BoardManager


# class TestBoardManager(unittest.TestCase):

#     def setUp(self):
#         """
#         Set up a new BoardManager instance before each test.
#         """

#         # Create a new BoardManager instance
#         self.trump_card = Card(Suit.HEARTS, Rank.ACE)  # ♥️A

#         # Set the trump card
#         self.board_manager = BoardManager(trump_card=self.trump_card)

#     def test_add_card_to_board(self):
#         """
#         Test adding a card to the board.
#         """

#         # Add a card to the board
#         card = Card(Suit.SPADES, Rank.TEN)  # ♠️10
#         self.board_manager.add_card_to_board(card)

#         # Check if the card is on the board
#         self.assertIn(card, self.board_manager.get_board_state())

#     def test_get_board_state(self):
#         """
#         Test getting the current state of the board.
#         """

#         # Add two cards to the board
#         card1 = Card(Suit.SPADES, Rank.TEN)  # ♠️10
#         card2 = Card(Suit.CLUBS, Rank.KING)  # ♣️K
#         self.board_manager.add_card_to_board(card1)
#         self.board_manager.add_card_to_board(card2)

#         # Check if the board state is correct
#         self.assertEqual(self.board_manager.get_board_state(), [card1, card2])

#     def test_get_board_ranks(self):
#         """
#         Test getting the ranks of all cards on the board.
#         """

#         card1 = Card(Suit.SPADES, Rank.TEN)
#         card2 = Card(Suit.CLUBS, Rank.KING)
#         self.board_manager.add_card_to_board(card1)
#         self.board_manager.add_card_to_board(card2)

#         # Check if the ranks are correct
#         self.assertEqual(self.board_manager.get_board_ranks(),
#                          {Rank.TEN, Rank.KING})

#     def test_clear_board(self):
#         """
#         Test clearing the board at the end of the round.
#         """

#         # Add a card to the board
#         card = Card(Suit.SPADES, Rank.TEN)  # ♠️10
#         self.board_manager.add_card_to_board(card)

#         # Clear the board
#         self.board_manager.clear_board()

#         # Check if the board is empty
#         self.assertEqual(self.board_manager.get_board_state(), [])

#     def test_is_board_full_first_round(self):
#         """
#         Test checking if the board is full in the first round.
#         """

#         # Add 10 cards to the board
#         for _ in range(10):
#             self.board_manager.add_card_to_board(Card(Suit.SPADES, Rank.TEN))

#         # Check if the board is full
#         self.assertTrue(self.board_manager.is_board_full())

#     def test_is_board_full_subsequent_rounds(self):
#         """
#         Test checking if the board is full in subsequent rounds.
#         """

#         # Move to the next round
#         self.board_manager.next_round()  # Move to round 2

#         # Add 12 cards to the board
#         for _ in range(12):
#             self.board_manager.add_card_to_board(Card(Suit.SPADES, Rank.TEN))

#         # Check if the board is full
#         self.assertTrue(self.board_manager.is_board_full())

#     def test_next_round(self):
#         """
#         Test moving to the next round.
#         """

#         # Add a card to the board
#         card = Card(Suit.SPADES, Rank.TEN)
#         self.board_manager.add_card_to_board(card)

#         # Move to the next round
#         self.board_manager.next_round()

#         # Check if the board is empty and the round number is incremented
#         self.assertEqual(self.board_manager.get_board_state(), [])
#         self.assertEqual(self.board_manager.round_number, 2)


# if __name__ == '__main__':
#     unittest.main()
