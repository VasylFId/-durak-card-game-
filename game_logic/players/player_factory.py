import logging
from game_logic.players.player import Player
from game_logic.players.strategies import (
    HumanAttackStrategy, HumanDefenseStrategy,
    AIAttackStrategy, AIDefenseStrategy
)

logger = logging.getLogger(__name__)


class PlayerFactory:
    @staticmethod
    def create_player(name: str, player_type: str) -> Player:
        """
        Factory method to create a Player instance based on type.

        Args:
            name (str): The name of the player.
            player_type (str): The type of player ('human' or 'ai').

        Returns:
            Player: An instance of Player with appropriate strategies.

        Raises:
            ValueError: If an unknown player type is provided.
        """
        if player_type == 'human':
            attack_strategy = HumanAttackStrategy()
            defense_strategy = HumanDefenseStrategy()
        elif player_type == 'ai':
            attack_strategy = AIAttackStrategy()
            defense_strategy = AIDefenseStrategy()
        else:
            logger.error(f"Unknown player type: {player_type}")
            raise ValueError(f"Unknown player type: {player_type}")

        player = Player(name, attack_strategy, defense_strategy)
        logger.info(f"Player created: {player.name} ({player_type})")
        return player
