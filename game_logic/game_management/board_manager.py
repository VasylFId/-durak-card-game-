import logging
from game_logic.card_package import Card

logger = logging.getLogger(__name__)


class BoardManager:
    def __init__(self, trump_card, initial_round: int = 1):
        self.board = []
        self.trump_card = trump_card
        self.round_number = initial_round

    def add_card_to_board(self, card: Card):
        """
        Adds a card to the board.

        Args:
            card (Card): The card to be added to the board.
        """
        self.board.append(card)
        logger.info(f"Card {card} added to the board.")

    def get_board_state(self) -> list:
        """
        Returns the current state of the board.

        Returns:
            list: The current state of the board.
        """
        return self.board

    def get_board_ranks(self) -> set:
        """
        Returns a set of the ranks of all cards on the board.

        Returns:
            set: A set of ranks currently on the board.
        """
        return {card.rank for card in self.board}

    def clear_board(self):
        """
        Clears the board at the end of the round.
        """
        self.board = []

    def is_board_full(self) -> bool:
        """
        Checks if the board is full based on the current round.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        max_cards = 10 if self.round_number == 1 else 12
        return len(self.board) >= max_cards

    def next_round(self):
        """
        Prepares the board for the next round by clearing the board and
        incrementing the round number.
        """
        self.clear_board()
        self.round_number += 1
        logger.info(f"Round {self.round_number} begins.")
