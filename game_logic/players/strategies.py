from abc import ABC, abstractmethod
from game_logic.card_package import Card
from game_logic.game_management import BoardManager


class AttackStrategy(ABC):
    @abstractmethod
    def select_card_to_attack(self, player, board_manager: BoardManager) -> Card:
        pass


class DefenseStrategy(ABC):
    @abstractmethod
    def select_card_to_defend(self, player, board_manager: BoardManager, attack_card: Card) -> Card:
        pass

# game_logic/players/strategies.py

class HumanAttackStrategy(AttackStrategy):
    def select_card_to_attack(self, player, board_manager: BoardManager) -> Card:
        # Implement user input logic for attacking
        pass


class HumanDefenseStrategy(DefenseStrategy):
    def select_card_to_defend(self, player, board_manager: BoardManager, attack_card: Card) -> Card:
        # Implement user input logic for defending against attack_card
        pass


class AIAttackStrategy(AttackStrategy):
    def select_card_to_attack(self, player, board_manager: BoardManager) -> Card:
        # Implement AI logic for selecting attack card
        # Example: Select the lowest possible card to attack
        if player.hand:
            return min(player.hand, key=lambda c: c.weight)
        return None


class AIDefenseStrategy(DefenseStrategy):
    def select_card_to_defend(self, player, board_manager: BoardManager, attack_card: Card) -> Card:
        # Implement AI logic for selecting defense card
        # Example: Select the minimal card that can beat the attack_card
        possible_defenses = [
            card for card in player.hand if card.can_beat(attack_card, player.trump_suit)
        ]
        return min(possible_defenses, key=lambda c: c.weight) if possible_defenses else None
