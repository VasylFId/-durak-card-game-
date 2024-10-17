import logging
from game_logic.card_package import Deck, Card
from game_logic.players.player_factory import PlayerFactory
from game_logic.game_management import RoundManager, PlayerManager, TrumpManager, RulesManager, DeckManager

logger = logging.getLogger(__name__)


class DurakGameManager:

    def __init__(self, player_configs: list):
        self.__init_managers()
        self.players = [PlayerFactory.create_player(config) for config in player_configs]
        self.__draw_cards()

    def __init_managers(self):
        self.deck = Deck()

    def __draw_cards(self):
        for player in self.players:
            PlayerManager.deal_initial_cards(self.deck, player, 6)

        DeckManager.reset_trump_card(self.deck)

        trump_card = DeckManager.get_trump_card(self.deck)
        
        PlayerManager.set_player_trump_suit(self.players[0], trump_card)
        PlayerManager.set_player_trump_suit(self.players[1], trump_card)

        for player in self.players:
            logger.info(f"{player.name} has the following trump card: {PlayerManager.get_player_trump_suit(player)}")

        if not TrumpManager.is_trump_card_valid(self.deck, self.players):
            TrumpManager.set_new_trump_card(self.deck, self.players)


    def run(self):
        pass
