import logging
from game_logic.game_management import PlayerManager, DeckManager
from game_logic.card_package import Deck

logger = logging.getLogger(__name__)


class RoundManager:
    round_number = 0
    roles_switched = False

    @staticmethod
    def initialize_round(attacker, defender, deck: Deck):
        """
        Initializes the round, dealing cards if necessary, and switching roles if needed.

        Args:
            attacker (Player): The player who is currently the attacker.
            defender (Player): The player who is currently the defender.
            deck (Deck): The deck of cards to deal from.
        """
        RoundManager.round_number += 1
        logger.info(f"Initializing round {RoundManager.round_number}.")

        # Switch roles if they were set to switch after the previous round
        if RoundManager.roles_switched:
            attacker, defender = defender, attacker
            RoundManager.roles_switched = False  # Reset switch flag
            logger.info("Roles switched. New Attacker: %s, New Defender: %s", attacker.name, defender.name)
        else:
            logger.info("Roles remain the same. Attacker: %s, Defender: %s", attacker.name, defender.name)

        return attacker, defender

    @staticmethod
    def finalize_round(roles_should_switch: bool):
        """
        Finalizes the round by determining whether roles should be switched in the next round.

        Args:
            roles_should_switch (bool): Whether roles should be switched for the next round.
        """
        RoundManager.roles_switched = roles_should_switch
        logger.info(f"Round {RoundManager.round_number} ended. Roles switching next round: {roles_should_switch}")

