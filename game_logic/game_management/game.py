# game.py

import logging
from game_logic.card_package import Deck, Card
from game_logic.players import Player
from game_logic.game_management import RoundManager, UserInputManager

logger = logging.getLogger(__name__)


class DurakGameManager:
    def __init__(self):
        """
        Initializes the DurakGameManager with a deck and players.
        """
        self.deck = Deck()
        self.players = [Player("Alice"), Player("Bob")]
        self.round_manager = RoundManager(self.deck, self.players)
        self.user_input_manager = UserInputManager()
        self.game_over = False

    def setup_game(self):
        """
        Sets up the game by dealing initial cards and setting the trump suit.
        """
        logger.info("Setting up the game.")
        self.round_manager.start_round()

    def play_round(self):
        """
        Plays a single round until it's over.
        """
        logger.info(f"Playing round {self.round_manager.round_number}.")

        while not self.round_manager.is_round_over():
            current_player = self.round_manager.get_current_player()

            if self.round_manager.is_attacker_turn:
                # Attacker's turn to attack
                attack_card = self.user_input_manager.get_card_from_player(
                    self.round_manager.board_manager,
                    self.round_manager.current_attacker,
                    context="attack",
                )

                if attack_card is None:
                    logger.info(f"{self.round_manager.current_attacker.name} chose to skip attack.")
                    break  # Attacker chooses to skip

                if self.round_manager.process_attack(attack_card):
                    logger.info(f"{self.round_manager.current_attacker.name} successfully attacked with {attack_card}.")
                else:
                    logger.warning("Failed to process attack.")
                    continue  # Retry attack

            elif self.round_manager.is_defender_turn:
                # Defender's turn to defend
                last_attack_card = (
                    self.round_manager.turn_manager.turn_state["attacks"][-1]
                    if self.round_manager.turn_manager.turn_state["attacks"]
                    else None
                )

                if last_attack_card is None:
                    logger.warning("No attack to defend against.")
                    break

                defense_card = self.user_input_manager.get_card_from_player(
                    self.round_manager.board_manager,
                    self.round_manager.current_defender,
                    context="defense",
                    attacking_card=last_attack_card,
                )

                if defense_card is None:
                    logger.info(f"{self.round_manager.current_defender.name} chose to fail defense.")
                    # Defender fails to defend; they pick up all cards on the board
                    self.pick_up_cards(self.round_manager.current_defender)
                    break

                if self.round_manager.process_defense(defense_card, last_attack_card):
                    logger.info(f"{self.round_manager.current_defender.name} successfully defended with {defense_card}.")
                else:
                    logger.warning("Failed to process defense.")
                    continue  # Retry defense

        logger.info(f"Round {self.round_manager.round_number} ended.")

    def pick_up_cards(self, player: Player):
        """
        Player picks up all cards on the board.

        Args:
            player (Player): The player picking up the cards.
        """
        board_cards = self.round_manager.board_manager.get_board_state()
        for card in board_cards:
            player.add_card_to_hand(card)
        self.round_manager.board_manager.clear_board()
        logger.info(f"{player.name} picked up all cards on the board.")

    def check_game_over(self):
        """
        Checks if the game is over and updates the game_over flag.
        """
        if self.round_manager.check_game_over():
            self.game_over = True
            winner = next((player for player in self.players if player.has_cards()), None)
            if winner:
                logger.info(f"Game over! {winner.name} wins!")
                print(f"Game over! {winner.name} wins!")
            else:
                logger.info("Game over! No winner.")
                print("Game over! No winner.")

    def prepare_next_round(self):
        """
        Prepares for the next round by resetting the board and switching roles.
        """
        self.round_manager.prepare_for_next_round()

    def run_game(self):
        """
        Runs the main game loop until the game is over.
        """
        self.setup_game()

        while not self.game_over:
            self.play_round()
            self.check_game_over()
            if not self.game_over:
                self.prepare_next_round()

        logger.info("Thank you for playing Durak!")
        print("Thank you for playing Durak!")


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Start the game
    game_manager = DurakGameManager()
    game_manager.run_game()
