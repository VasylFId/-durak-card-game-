import logging

from game_logic.card_package import Deck
from game_logic.players.player import Player
# from game_logic.players.player_factory import PlayerFactory
from game_logic.game_management import BoardManager, DeckManager
from game_logic.game_management import PlayerManager, RoundManager
from game_logic.game_management import RulesManager, SessionManager
from game_logic.game_management import TrumpManager, TurnManager
from game_logic.game_management import UserInputManager


logger = logging.getLogger(__name__)


class DurakGameManager:

    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]
        self.deck = Deck()
        self.__init_managers()
        self.__deal_initial_cards()
        self.__check_trump_card()
        self.__initialise_roles()

    def __init_managers(self):
        self.player_manager = PlayerManager()
        self.deck_manager = DeckManager()
        self.round_manager = RoundManager()
        self.rules_manager = RulesManager()
        # self.session_manager = SessionManager()
        self.trump_manager = TrumpManager()
        # self.turn_manager = TurnManager()
        self.user_input_manager = UserInputManager()

    def __deal_initial_cards(self):
        for player in self.players:
            self.player_manager.deal_initial_cards(self.deck, player, 6)

        self.deck_manager.reset_trump_card(self.deck)

        trump_card = DeckManager.get_trump_card(self.deck)

        for player in self.players:
            self.player_manager.set_player_trump_suit(player, trump_card)

    def __check_trump_card(self):

        self.trump_card = self.deck_manager.get_trump_card(self.deck)

        if not self.trump_manager.is_trump_card_valid(self.deck, self.players):
            self.trump_card = self.trump_manager.set_new_trump_card(
                self.deck, self.players)

            for player in self.players:
                self.player_manager.set_player_trump_suit(player,
                                                          self.trump_card)

        # Log information about the update of the trump card

        logger.info("Trump card is succesfully reset.")

        self.board_manager = BoardManager(trump_card=self.trump_card)

    def __initialise_roles(self):
        # Determine the roles of the players
        self.attacker = self.player_manager.get_lowest_trump_card_player(
            self.players, self.trump_card)
        self.defender = self.player_manager.get_defender(self.players,
                                                         self.attacker)

        # Log the roles of the players
        logger.info("Attacker: %s", self.player_manager.get_player_name(
            self.attacker))
        logger.info("Defender: %s", self.player_manager.get_player_name(
            self.defender))

    def run(self):
        logger.info("Starting the game...")

        self.attacker, self.defender = self.round_manager.initialize_round(
            self.attacker, self.defender, self.deck)

        self.board_manager = BoardManager(trump_card=self.trump_card)

        while not self.rules_manager.is_game_over(len(self.deck),
                                                  *self.players):
            logger.info("Starting a new round...")

            self.board_manager.clear_board()

            if self.round_manager.round_number != 1:
                self.attacker, self.defender = \
                    self.round_manager.initialize_round(
                        self.attacker, self.defender, self.deck)

            while not self.rules_manager.is_round_over(self.players,
                                                       self.board_manager):
                self.turn_manager = TurnManager(
                    attacker=self.attacker, defender=self.defender,
                    board_manager=self.board_manager)

                card_to_attack = self.user_input_manager.get_card_from_player(
                    self.board_manager, self.attacker, "attack")

                if not card_to_attack:
                    switch_roles = True
                    self.round_manager.finalize_round(switch_roles)
                    self.board_manager.next_round()
                    continue

                self.turn_manager.execute_attack(card_to_attack)

                card_to_defend = self.user_input_manager.get_card_from_player(
                    self.board_manager, self.defender, "defense",
                    card_to_attack)

                if not card_to_defend:
                    self.round_manager.finalize_round()
                    self.board_manager.next_round()
                    continue

                self.turn_manager.handle_defense(card_to_attack,
                                                 card_to_defend)
                # self.turn_manager.switch_turn()


if __name__ == "__main__":
    # Players setup
    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game = DurakGameManager(player1=player1, player2=player2)
    game.run()
