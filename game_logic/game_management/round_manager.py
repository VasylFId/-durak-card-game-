"""
This module contains the RoundManager class, which is responsible for managing
the rounds in the game.

Classes:
    RoundManager: A class for managing the rounds in the game.

Usage:
    RoundManager.initialize_round(attacker, defender, deck)
    RoundManager.finalize_round(roles_should_switch)
"""


import logging
# from game_logic.game_management import PlayerManager, DeckManager
from game_logic.card_package import Deck

logger = logging.getLogger(__name__)


class RoundManager:
    """
    A class for managing the rounds in the game.

    Attributes:
        round_number (int): The current round number.
        roles_switched (bool): Whether roles were switched in the previous
                            round.

    Methods:
        initialize_round(attacker, defender, deck):
            Initializes the round, dealing cards if necessary, and switching
            roles if needed.
        finalize_round(roles_should_switch):
            Finalizes the round by determining whether roles should be
            switched in the next
    """

    round_number = 1
    roles_switched = False

    @staticmethod
    def initialize_round(attacker, defender, deck: Deck):
        """
        Initialize a new round, switching attacker and defender if needed.
        
        Args:
            attacker: Current attacker
            defender: Current defender
            deck: Game deck
            
        Returns:
            tuple: The (potentially swapped) attacker and defender
        """
        logger.info(f"\n\nInitializing round {RoundManager.round_number+1}.")
        
        if RoundManager.roles_switched:
            logger.info("Roles will be switched for next round")
            attacker, defender = defender, attacker
            RoundManager.roles_switched = False
            logger.info(f"Roles switched. New Attacker: {attacker.name}, New Defender: {defender.name}")
        else:
            logger.info(f"Roles remain the same. Attacker: {attacker.name}, Defender: {defender.name}")
        
        return attacker, defender

    @staticmethod
    def finalize_round(roles_should_switch: bool = False):
        """
        Finalizes the current round and prepares for the next round.
        
        Args:
            roles_should_switch (bool): Whether to switch attacker and defender roles in the next round.
        """

        # First store whether roles will switch
        RoundManager.roles_switched = roles_should_switch
        
        # Log round end with current round number
        logger.info(f"Round {RoundManager.round_number} ended. Roles switching next round: {roles_should_switch}")
        
        # Increment round number AFTER logging
        RoundManager.round_number += 1
        
        return RoundManager.roles_switched
