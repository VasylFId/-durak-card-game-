"""
This module contains the RulesManager class, which is responsible for enforcing
the rules of the game.

Classes:
    RulesManager: A class for enforcing the rules of the game.

Usage:
    rules_manager = RulesManager()
    valid_attack = rules_manager.is_valid_attack(board_manager, card)
    valid_defense = rules_manager.is_valid_defense(board_manager, attack_card,
                                                   defense_card)
    board_full = rules_manager.is_board_full(board_manager)
    card_distribution = RulesManager.determine_card_distribution(deck_size,
                                                            attacker, defender)
"""


import logging
from game_logic.card_package import Card
from game_logic.players import Player
from game_logic.game_management import BoardManager

logger = logging.getLogger(__name__)


class RulesManager:
    @staticmethod
    def is_valid_attack(board_manager: BoardManager, card: Card) -> bool:
        """
        Checks if the attack is valid based on the game rules.

        Args:
            board_manager (BoardManager): The manager that holds the current
                                          state of the board.
            card (Card): The card being played by the attacker.

        Returns:
            bool: True if the attack is valid, False otherwise.
        """
        board_ranks = board_manager.get_board_ranks()

        # An attack is valid if the rank of the card being played matches any
        # rank on the board, or if the board is empty (first move).
        if not board_ranks or card.rank in board_ranks:
            logger.info(f"Attack with {card} is valid.")
            return True
        else:
            logger.warning(f"Invalid attack with {card}. No matching rank on" +
                           f" the board: {board_ranks}.")
            return False

    @staticmethod
    def is_valid_defense(board_manager: BoardManager,
                         attack_card: Card,
                         defense_card: Card) -> bool:
        """
        Checks if the defense is valid based on the game rules.

        Args:
            board_manager (BoardManager): The manager that holds the current
                                          state of the board.
            attack_card (Card): The card that was played by the attacker.
            defense_card (Card): The card being played by the defender.

        Returns:
            bool: True if the defense is valid, False otherwise.
        """

        trump_suit = board_manager.trump_card.suit

        # Use the card's compare method to determine if the defense is valid.
        comparison = defense_card.compare(attack_card, trump_suit)

        if comparison > 0:
            logger.info(f"Defense with {defense_card} is valid; it beats " +
                        f"{attack_card}.")
            return True
        else:
            logger.warning(f"Invalid defense with {defense_card}; cannot " +
                           f"beat {attack_card}.")
            return False

    @staticmethod
    def is_board_full(board_manager: BoardManager) -> bool:
        """
        Checks if the board is full based on the current round.

        Args:
            board_manager (BoardManager): The manager that holds the current
                                          state of the board.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return board_manager.is_board_full()

    def determine_card_distribution(deck_size: int, attacker: Player,
                                    defender: Player) -> dict:
        """
        Determines how many cards each player should pick up from the deck.

        Args:
            deck_size (int): The number of cards remaining in the deck.
            attacker (Player): The attacking player.
            defender (Player): The defending player.

        Returns:
            dict: A dictionary with keys 'attacker' and 'defender' indicating
                  how many cards each player should pick up.
        """

        # Determine how many cards each player needs
        attacker_needed = max(0, 6 - len(attacker.hand))
        defender_needed = max(0, 6 - len(defender.hand))

        # Determine how to distribute the cards
        if attacker_needed == 0 and defender_needed == 0:
            return {"attacker": 0, "defender": 0}

        elif attacker_needed == 0:
            return {"attacker": 0, "defender": min(deck_size, defender_needed)}

        elif defender_needed == 0:
            return {"attacker": min(deck_size, attacker_needed), "defender": 0}

        # Both need cards
        total_needed = attacker_needed + defender_needed

        if total_needed <= deck_size:
            # Enough cards to satisfy both
            return {"attacker": attacker_needed, "defender": defender_needed}
        else:
            # Not enough cards, split fairly
            attacker_share = min(attacker_needed, deck_size // 2)
            defender_share = min(defender_needed, deck_size - attacker_share)
            return {"attacker": attacker_share, "defender": defender_share}

    @staticmethod
    def is_game_over(deck_size: int,
                     attacker: Player,
                     defender: Player) -> bool:
        """
        Checks if the game is over based on the current state of the game.

        Args:
            deck_size (int): The number of cards remaining in the deck.
            attacker (Player): The attacking player.
            defender (Player): The defending player.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return deck_size == 0 and not attacker.has_cards() and \
            not defender.has_cards()

    @staticmethod
    def is_round_over(players: list, board_manager: BoardManager) -> bool:
        """
        Checks if the round is over based on the current state of the board.

        Args:
            players (list): A list of all players in the game.
            board_manager (BoardManager): The manager that holds the current
                                          state of the board.

        Returns:
            bool: True if the round is over, False otherwise.
        """
        return all(not player.has_cards() for player in players) or \
            board_manager.is_board_full()
