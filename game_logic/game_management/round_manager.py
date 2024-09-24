# round_manager.py

import logging
from game_logic.game_management import (
    BoardManager, DeckManager, PlayerManager, TurnManager, UserInputManager
)

from game_logic.card_package import Deck, Card

logger = logging.getLogger(__name__)


class RoundManager:
    def __init__(self, deck: Deck, players: list):
        """
        Initializes the RoundManager with a deck of cards and a list of players.

        Args:
            deck (Deck): The deck of cards for the round.
            players (list[Player]): The players participating in the game.

        Attributes:
            deck (Deck): The deck of cards for the round.
            players (list[Player]): The players in the game.
            board_manager (BoardManager): Manages the game board state.
            turn_manager (TurnManager): Manages player turns.
            round_number (int): The current round number.
            user_input_manager (UserInputManager): Manages user input.
        """
        self.deck = deck
        self.players = players
        self.board_manager = BoardManager(self.deck.trump_card)
        self.turn_manager = None
        self.round_number = 1
        self.user_input_manager = UserInputManager()

    def start_round(self):
        """
        Starts a new round by initializing the attacking and defending players
        and dealing cards if necessary.
        """
        logger.info(f"Starting round {self.round_number}.")

        # Assign attacker and defender
        self.current_attacker = self.players[0]
        self.current_defender = self.players[1]
        logger.info(
            f"{self.current_attacker.name} attacks, {self.current_defender.name} defends."
        )

        # Initialize turn manager with BoardManager
        self.turn_manager = TurnManager(
            self.current_attacker, self.current_defender, self.board_manager
        )

        # Deal cards if needed
        for player in self.players:
            if len(PlayerManager.get_player_hand(player)) < 6:
                DeckManager.reshuffle_if_needed(self.deck)
                PlayerManager.deal_initial_cards(self.deck, player)

    def is_round_over(self):
        """
        Determines if the round is over based on the number of cards on the board.

        Returns:
            bool: True if the round is over, False otherwise.
        """
        return self.board_manager.is_board_full()

    def process_attack(self, attack_card: Card) -> bool:
        """
        Processes the attacking player's move.

        Args:
            attack_card (Card): The card played by the attacker.

        Returns:
            bool: True if the attack was successful, False otherwise.
        """
        if not self.turn_manager.execute_attack(attack_card):
            logger.warning(
                f"{self.current_attacker.name} played invalid attack: {attack_card}."
            )
            return False
        return True

    def process_defense(self, defense_card: Card, attack_card: Card) -> bool:
        """
        Processes the defending player's move.

        Args:
            defense_card (Card): The card played by the defender.
            attack_card (Card): The card played by the attacker.

        Returns:
            bool: True if the defense was successful, False otherwise.
        """
        if not self.turn_manager.handle_defense(attack_card, defense_card):
            logger.warning(
                f"{self.current_defender.name} played invalid defense: {defense_card}."
            )
            return False
        return True

    def get_current_player(self):
        """
        Gets the current player whose turn it is to play.

        Returns:
            Player: The current attacking or defending player.
        """
        if self.turn_manager.is_attacker_turn:
            return self.current_attacker
        else:
            return self.current_defender

    def prepare_for_next_round(self):
        """
        Prepares for the next round by resetting the board, dealing cards if needed,
        and switching attacker and defender.
        """
        logger.info(f"Preparing for round {self.round_number + 1}.")
        self.board_manager.clear_board()
        self.round_number += 1

        # Switch attacker and defender
        self.current_attacker, self.current_defender = (
            self.current_defender,
            self.current_attacker,
        )
        logger.info(
            f"Next round: {self.current_attacker.name} attacks, "
            f"{self.current_defender.name} defends."
        )

        # Reset TurnManager with new attacker and defender
        self.turn_manager = TurnManager(
            self.current_attacker, self.current_defender, self.board_manager
        )

        # Deal cards if needed
        for player in self.players:
            if len(PlayerManager.get_player_hand(player)) < 6:
                DeckManager.reshuffle_if_needed(self.deck)
                PlayerManager.deal_initial_cards(self.deck, player)

    def check_game_over(self) -> bool:
        """
        Checks if the game is over by verifying if a player has no cards left
        or deck is empty.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        # A player has no cards
        for player in self.players:
            if not player.has_cards() and self.deck.is_empty():
                logger.info(f"Game over! {player.name} has no cards left.")
                return True

        # Alternatively, if the deck is empty and players cannot replenish
        # (Depending on game rules, this can be adjusted)
        return False
