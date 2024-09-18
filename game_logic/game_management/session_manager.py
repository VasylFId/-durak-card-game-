"""Session Manager Module
"""


class SessionManager:
    """Session Manager Class
    """

    def __init__(self, player_manager, deck_manager, board_manager, rules_manager, turn_manager, trump_manager):
        """Constructor for Session Manager
        """
        self.player_manager = player_manager
        self.deck_manager = deck_manager
        self.board_manager = board_manager
        self.rules_manager = rules_manager
        self.turn_manager = turn_manager
        self.trump_manager = trump_manager

    def start_game(self):
        """Starts the game
        """
        self.deck_manager.shuffle_deck()
        self.deck_manager.deal_cards()
        self.trump_manager.set_trump()
        self.turn_manager.set_starting_player
        self.turn_manager.start_turn()

    def end_game(self):
        """Ends the game
        """
        pass
