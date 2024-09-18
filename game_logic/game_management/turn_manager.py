import logging
from game_logic.card_package import Card
from game_logic.players import Player
from game_logic.game_management import PlayerManager, RulesManager

logger = logging.getLogger(__name__)


class TurnManager:
    def __init__(self, attacker: Player, defender: Player, board_manager):
        """
        Initializes the TurnManager with the current attacking and defending players.

        Args:
            attacker (Player): The player who will attack first.
            defender (Player): The player who will defend first.
            board_manager (BoardManager): The manager that holds the current state of the board.
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

    def switch_turn(self):
        """
        Switches the turn between the attacking and defending players.
        """
        if self.attack_completed or self.defense_completed:
            self.is_attacker_turn = not self.is_attacker_turn
            self.is_defender_turn = not self.is_defender_turn
            logger.info(f"Turn switched: {'Attacker' if self.is_attacker_turn else 'Defender'}'s turn")
            self.attack_completed = False
            self.defense_completed = False

    def execute_attack(self, card: Card):
        """
        Handles the logic for the attacking player to make a move.

        Args:
            card (Card): The card played by the attacker.
        """
        if not self.is_attacker_turn:
            logger.warning("It's not the attacker's turn!")
            return False

        # Check if the attack is valid according to the game rules
        if RulesManager.is_valid_attack(self.board_manager, card):
            # Attacker plays a card
            PlayerManager.remove_card_from_hand(self.attacker, card)
            self.turn_state["attacks"].append(card)
            self.board_manager.add_card_to_board(card)
            logger.info(f"{self.attacker.name} attacks with {card}")
            self.attack_completed = True
            self.switch_turn()  # Switch to defender's turn
            return True
        else:
            logger.warning(f"{self.attacker.name}'s attack with {card} is invalid.")
            return False

    def handle_defense(self, attack_card: Card, defense_card: Card):
        """
        Handles the logic for the defending player to respond to the attack.

        Args:
            defense_card (Card): The card played by the defender.
        """
        if not self.is_defender_turn:
            logger.warning("It's not the defender's turn!")
            return False

        if not self.turn_state["attacks"]:
            logger.warning("No attack to defend against!")
            return False

        # Check if the defense is valid according to the game rules
        if RulesManager.is_valid_defense(self.board_manager, attack_card, defense_card):
            # Defender plays a card
            PlayerManager.remove_card_from_hand(self.defender, defense_card)
            self.turn_state["defenses"].append(defense_card)
            self.board_manager.add_card_to_board(defense_card)
            logger.info(f"{self.defender.name} defends with {defense_card}")
            self.defense_completed = True
            self.switch_turn()  # Switch to attacker's turn
            return True
        else:
            logger.warning(f"{self.defender.name}'s defense with {defense_card} is invalid.")
            return False

    def update_turn_state(self):
        """
        Updates the state of the turn, tracking which player is active and what actions have been taken.
        """
        logger.info(f"Current turn state: {self.turn_state}")
