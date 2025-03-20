"""
This module contains the BoardManager class, which is responsible for managing
the board in the game.

Classes:
    BoardManager: A class for managing the board in the game.

Usage:
    board_manager = BoardManager(trump_card)
    board_manager.add_card_to_board(card)
    board_manager.get_board_state()
    board_manager.get_board_ranks()
    board_manager.clear_board()
    board_manager.is_board_full()
    board_manager.next_round()
"""


import logging
from game_logic.card_package import Card

logger = logging.getLogger(__name__)


class BoardManager:

    """
    A class for managing the board in the game.

    Attributes:
        board (list of Card): The list of cards on the board.
        trump_card (Card): The trump card for the game.
        round_number (int): The current round number.

    Methods:
        add_card_to_board(card: Card) -> None:
            Adds a card to the board.
        get_board_state() -> list:
            Returns the current state of the board.
        get_board_ranks() -> set:
            Returns a set of the ranks of all cards on the board.
        clear_board() -> None:
            Clears the board at the end of the round.
        is_board_full() -> bool:
            Checks if the board is full based on the current round.
        next_round() -> None:
            Prepares the board for the next round.
    """

    def __init__(self, trump_card, initial_round: int = 1):
        """
        Initializes the board with an empty list of cards, a trump card, and
        the initial round number.

        Args:
            trump_card (Card): The trump card for the game.
            initial_round (int): The initial round number.
        """

        self.__board = []
        self.__discard_pile = []
        self.__trump_card = trump_card
        self.__round_number = initial_round

    def add_card_to_board(self, card: Card) -> None:
        """
        Adds a card to the board.

        Args:
            card (Card): The card to be added to the board.
        """

        self.__board.append(card)
        logger.info(f"Card {card} added to the board.")

    def get_board_state(self) -> list:
        """
        Returns the current state of the board.

        Returns:
            list: The current state of the board.
        """

        return self.__board

    def get_board_ranks(self) -> set:
        """
        Returns a set of the ranks of all cards on the board.

        Returns:
            set: A set of ranks currently on the board.
        """

        return {card.rank for card in self.__board}
    
    def get_last_attack_card(self) -> Card:
        """
        Returns the last attack card on the board.

        Returns:
            Card: The last attack card on the board.
        """

        # If there's an odd number of cards, the last one is an attack card
        if len(self.__board) % 2 == 1:  
            return self.__board[-1]
        return None
    
    def move_to_discard_pile(self) -> None:
        """Move all cards from the board to the discard pile"""
        self.__discard_pile.extend(self.__board)
        logger.info(f"Moved {len(self.__board)} cards to discard pile. " +
                    f"Discard pile now contains {len(self.__discard_pile)} " +
                    f"cards.")
        self.clear_board()

    def get_discard_pile(self) -> list:
        """
        Get all cards in the discard pile.
        
        Returns:
            list: Cards in the discard pile
        """
        return self.__discard_pile
    

    def clear_board(self) -> None:
        """
        Clears the board at the end of the round.
        """

        self.__board = []

    def is_board_full(self) -> bool:
        """
        Checks if the board is full based on the current round.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        max_cards = 10 if self.__round_number == 1 else 12
        return len(self.__board) >= max_cards

    def next_round(self):
        """
        Prepares the board for the next round by clearing the board and
        incrementing the round number.
        """
        if self.__board:
            self.move_to_discard_pile()
            
        # Increment the round number
        self.__round_number += 1
        logger.info(f"Moving to round {self.__round_number}")

    @property
    def round_number(self):
        """
        Property that returns the current round number.

        Returns:
            int: The current round number.
        """

        return self.__round_number

    @property
    def trump_card(self):
        """
        Property that returns the trump card.

        Returns:
            Card: The trump card.
        """

        return self.__trump_card
