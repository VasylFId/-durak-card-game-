"""
This module contains the TurnManager class, which is responsible for managing
the turns in the game.

Classes:
    TurnManager: A class for managing the turns in the game.

Usage:
    turn_manager = TurnManager(attacker, defender, board_manager)
    turn_manager.execute_attack(card)
    turn_manager.handle_defense(attack_card, defense_card)
    turn_manager.update_turn_state()
"""


import logging
from game_logic.card_package import Card
from game_logic.players import Player
from game_logic.game_management import BoardManager
from game_logic.game_management import PlayerManager, RulesManager

logger = logging.getLogger(__name__)


class TurnManager:
    """
    A class for managing the turns in the game.

    Methods:
        switch_turn():
            Switches the turn between the attacking and defending players.
        execute_attack(card):
            Handles the logic for the attacking player to make a move.
        handle_defense(attack_card, defense_card):
            Handles the logic for the defending player to respond to the attack
        update_turn_state():
            Updates the state of the turn, tracking which player is active and
            what actions have been taken.
    """

    def __init__(self, attacker: Player, defender: Player,
                 board_manager: BoardManager):
        """
        Initializes the TurnManager with the current attacking and defending
        players.

        Args:
            attacker (Player): The player who will attack first.
            defender (Player): The player who will defend first.
            board_manager (BoardManager): The manager that holds the current
            state of the board.
        """

        self.attacker = attacker
        self.defender = defender
        self.is_attacker_turn = True
        self.is_defender_turn = False
        self.attack_completed = False
        self.defense_completed = False
        self.turn_state = {
            "attacks": [],
            "defenses": []
        }
        self.board_manager = board_manager

    def switch_turn(self) -> None:
        """
        Switches the turn between the attacking and defending players.
        """

        # Switch turns only if the attack or defense has been completed
        if self.attack_completed or self.defense_completed:

            # Switch turns
            self.is_attacker_turn = not self.is_attacker_turn
            self.is_defender_turn = not self.is_defender_turn

            # Update the current attacker and defender
            turn = 'Attacker' if self.is_attacker_turn else 'Defender'
            logger.info(f"Turn switched: {turn}'s turn")

            # Reset the attack and defense flags
            self.attack_completed = False
            self.defense_completed = False

    def reset_turn_state(self):
        """
        Resets the turn state for the next turn.
        """

        self.turn_state = {
            "attacks": [],
            "defenses": []
        }
        # Start with attacker's turn
        self.is_attacker_turn = True
        self.is_defender_turn = False
        self.attack_completed = False
        self.defense_completed = False
        logger.info(f"Turn state reset - attacker ({self.attacker.name}) turn")

    def set_players(self, attacker: Player, defender: Player):
        """
        Sets the attacking and defending players for the next turn.

        Args:
            attacker (Player): The player who will attack first.
            defender (Player): The player who will defend first.
        """
        self.attacker = attacker
        self.defender = defender
        logger.info(f"TurnManager updated - Attacker: {attacker.name}, " +
                    f"Defender: {defender}")
        # Reset turn state for the new players
        self.reset_turn_state()

    def execute_attack(self, card: Card) -> bool:
        """
        Handles the logic for the attacking player to make a move.

        Args:
            card (Card): The card played by the attacker.

        Returns:
            bool: True if the attack is successful, False otherwise.
        """

        # Check if it's the attacker's turn
        if not self.is_attacker_turn:
            logger.warning("It's not the attacker's turn!")
            return False

        # Check if the attack is valid according to the game rules
        if RulesManager.is_valid_attack(self.board_manager, card):

            # Attacker plays a card
            PlayerManager.remove_card_from_hand(self.attacker, card)

            # Add the card to the board
            self.turn_state["attacks"].append(card)
            self.board_manager.add_card_to_board(card)

            logger.info(f"{self.attacker.name} attacks with {card}")

            # Update the turn state
            self.attack_completed = True

            # Switch to defender's turn
            self.switch_turn()

            return True
        else:
            logger.warning(f"{self.attacker.name}'s attack with {card}" +
                           " is invalid.")
            return False

    def handle_defense(self, attack_card: Card, defense_card: Card) -> bool:
        """
        Handles the logic for the defending player to respond to the attack.

        Args:
            defense_card (Card): The card played by the defender.
            attack_card (Card): The card played by the attacker.

        Returns:
            bool: True if the defense is successful, False otherwise.
        """

        logger.info(f"{self.defender.name} defends against {attack_card} " +
                    f"with {defense_card}")

        # Check if it's the defender's turn
        if not self.is_defender_turn:
            logger.warning("It's not the defender's turn!")
            return False

        # Check if the defender has a valid defense
        if not self.turn_state["attacks"]:
            logger.warning("No attack to defend against!")
            return False

        # Check if the defense is valid according to the game rules
        if RulesManager.is_valid_defense(self.board_manager,
                                         attack_card, defense_card):

            # Defender plays a card
            PlayerManager.remove_card_from_hand(self.defender, defense_card)

            # Add the card to the board
            self.turn_state["defenses"].append(defense_card)

            # Add the card to the board
            self.board_manager.add_card_to_board(defense_card)
            logger.info(f"{self.defender.name} defends with {defense_card}")

            # Update the turn state
            self.defense_completed = True

            # Switch to attacker's turn
            self.switch_turn()

            return True
        else:
            logger.warning(f"{self.defender.name}'s defense with " +
                           f"{defense_card} is invalid.")
            return False

    def update_turn_state(self):
        """
        Updates the state of the turn, tracking which player is active
        and what actions have been taken.
        """
        logger.info(f"Current turn state: {self.turn_state}")
