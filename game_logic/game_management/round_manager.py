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

    round_number = 0
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
            # Explicitly swap attacker and defender
            attacker, defender = defender, attacker
            RoundManager.roles_switched = False
            logger.info("Roles switched. New Attacker: %s, New Defender: %s",
                attacker.name, defender.name)
        else:
            logger.info("Roles remain the same. Attacker: %s, Defender: %s",
                attacker.name, defender.name)
                
        return attacker, defender
    
    @staticmethod
    def finalize_round(roles_should_switch: bool = False):
        """
        Finalizes the current round and prepares for the next round.
        
        Args:
            roles_should_switch (bool): Whether to switch attacker and defender roles in the next round.
        """
        # Store whether roles should be switched for the next round
        RoundManager.roles_switched = roles_should_switch
        logger.info(f"Round {RoundManager.round_number} ended." +
            f" Roles switching next round: {roles_should_switch}")
        
        # Increment the round number
        RoundManager.round_number += 1
