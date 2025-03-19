import logging

from game_logic.card_package import Deck
from game_logic.players.player import Player
from game_logic.game_management.board_manager import BoardManager
from game_logic.game_management.deck_manager import DeckManager
from game_logic.game_management.player_manager import PlayerManager
from game_logic.game_management.round_manager import RoundManager
from game_logic.game_management.rules_manager import RulesManager
from game_logic.game_management.trump_manager import TrumpManager
from game_logic.game_management.turn_manager import TurnManager
from game_logic.game_management.user_input_manager import UserInputManager


logger = logging.getLogger(__name__)


class DurakGameManager:
    """
    Main game manager class for the Durak card game.
    This class coordinates all aspects of the game including:
    - Game initialization
    - Player management
    - Card dealing
    - Game flow control
    - Turn management
    """

    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]
        self.deck = Deck()
        self.__init_managers()
        self.__setup_game()
        
        # Initialize initial board manager
        self.board_manager = BoardManager(trump_card=self.trump_card)
        
        # Initialize the turn manager directly here (this was missing)
        self.turn_manager = TurnManager(
            attacker=self.attacker,
            defender=self.defender,
            board_manager=self.board_manager
        )

    def __init_managers(self):
        """Initialize all game component managers"""
        self.player_manager = PlayerManager()
        self.deck_manager = DeckManager()
        self.round_manager = RoundManager()
        self.rules_manager = RulesManager()
        # self.session_manager = SessionManager()  # Currently not used
        self.trump_manager = TrumpManager()
        # self.turn_manager initialized later
        self.user_input_manager = UserInputManager()

    def __setup_game(self):
        """Setup the game by dealing cards, setting up trump and initializing roles"""
        self.__deal_initial_cards()
        self.__setup_trump_card()
        self.__initialize_roles()
        
    def __deal_initial_cards(self):
        """Deal initial cards to all players"""
        for player in self.players:
            self.player_manager.deal_initial_cards(self.deck, player, 6)

        self.deck_manager.reset_trump_card(self.deck)

        trump_card = DeckManager.get_trump_card(self.deck)

        for player in self.players:
            self.player_manager.set_player_trump_suit(player, trump_card)

    def __setup_trump_card(self):
        """Validate and potentially reset the trump card"""
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

    def __initialize_roles(self):
        """Determine the initial roles of the players (attacker/defender)"""
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
        
    def deal_cards_to_player(self, player, quantity):
        """
        Deal a specified number of cards to a player
        
        Args:
            player (Player): The player to deal cards to
            quantity (int): The number of cards to deal
        """
        for _ in range(quantity):
            if DeckManager.can_draw_card_to_player(self.deck):
                card = DeckManager.draw_card(self.deck)
                logger.info(f"Dealt {card} to {player.name}")
                PlayerManager.add_card_to_hand(player, card)
            elif DeckManager.get_trump_card(self.deck):
                card = DeckManager.draw_trump_card(self.deck)
                logger.info(f"Dealt {card} to {player.name}")
                PlayerManager.add_card_to_hand(player, card)
            else:
                logger.warning("Deck is empty; cannot deal more cards.")
                break

    def __setup_round(self):
        """Setup a new round by clearing the board and dealing cards"""
        logger.info("Starting a new round...")
        
        # Clear the board for the new round
        self.board_manager.clear_board()

        # Deal cards to players (except for the first round which was handled in initialization)
        if self.round_manager.round_number != 0:
            self.attacker, self.defender = self.round_manager.initialize_round(
                self.attacker, self.defender, self.deck)

            # Calculate how many cards to deal based on deck size
            trump_card_drawn = self.deck.trump_card is not None
            deck_size = len(self.deck) + int(trump_card_drawn)

            card_distribution = self.rules_manager.determine_card_distribution(
                deck_size, self.attacker, self.defender)

            logger.info(f"Card distribution: {card_distribution}")

            # Deal cards to both players
            self.deal_cards_to_player(self.attacker, card_distribution['attacker'])
            self.deal_cards_to_player(self.defender, card_distribution['defender'])

        logger.info(f"Round {self.round_manager.round_number + 1} begins.")
        
        # Initialize turn manager for this round
        self.turn_manager = TurnManager(
            attacker=self.attacker,
            defender=self.defender,
            board_manager=self.board_manager
        )
    
    def __handle_attack(self):
        """Handle the attack phase of a turn
        
        Returns:
            bool: True if attack is valid, False if attacker passes
        """
        card_to_attack = self.user_input_manager.get_card_from_player(
            self.board_manager, self.attacker, "attack")

        logger.info("Card to attack: %s", card_to_attack)

        # If attacker passes or has no valid cards, round ends successfully for defender
        if card_to_attack is None:
            logger.info("Attacker passes - round ends successfully")
            self.round_manager.finalize_round(switch_roles=True)
            self.board_manager.next_round()
            return False

        # Process the attack
        self.turn_manager.execute_attack(card_to_attack)
        return True
    
    def __handle_defense(self, card_to_attack):
        """Handle the defense phase of a turn
        
        Args:
            card_to_attack: The card that is being defended against
            
        Returns:
            bool: True if defense is successful, False if defender takes cards
        """
        card_to_defend = self.user_input_manager.get_card_from_player(
            self.board_manager, self.defender, "defense", card_to_attack)

        logger.info("Card to defend: %s", card_to_defend)

        # If defender cannot or chooses not to defend, they pick up all cards
        if card_to_defend is None:
            logger.info("Defender takes cards - round ends")
            # Original code doesn't pass switch_roles parameter here
            self.round_manager.finalize_round()
            
            # Add all board cards to defender's hand
            board_cards = self.board_manager.get_board_state()
            for board_card in board_cards:
                PlayerManager.add_card_to_hand(self.defender, board_card)
            
            self.board_manager.next_round()
            return False

        # Process the defense
        self.turn_manager.handle_defense(card_to_attack, card_to_defend)
        return True
    
    def __check_attack_continuation(self):
        """Check if additional attacks are possible
        
        Returns:
            bool: True if round continues, False if round ends
        """
        if not self.rules_manager.can_attack_again(self.attacker, self.board_manager):
            logger.info("No more valid attacks possible - round ends")
            self.round_manager.finalize_round(switch_roles=True)
            self.board_manager.clear_board()
            return False
        return True
    
    def __check_win_condition(self):
        """Check if the game has a winner
        
        Returns:
            bool: True if game is over, False if game continues
        """
        if self.rules_manager.check_win_condition(self.players, self.deck):
            winner = self.rules_manager.get_winner(self.players, self.deck)
            if winner:
                logger.info(f"Game over! Winner: {winner.name}")
            else:
                logger.info("Game over! It's a draw.")
            return True
        return False
    
    def __play_round(self):
        """Play one complete round of Durak
        
        Returns:
            bool: True if game should continue, False if game is over
        """
        # Round loop (attack-defense cycle)
        while not self.rules_manager.is_round_over(self.players, self.board_manager):
            # Attack phase
            if not self.__handle_attack():
                break
                
            # Defense phase
            card_to_attack = self.board_manager.get_last_attack_card()
            if not self.__handle_defense(card_to_attack):
                break
                
            # Check if additional attacks are possible
            if not self.__check_attack_continuation():
                break
        
        # End of round processing
        logger.info(f"Round {self.round_manager.round_number} completed")
        
        # Check win conditions
        return not self.__check_win_condition()
    
    def run(self):
        """Run the main game loop"""
        logger.info("Starting the game...")

        # Initialize the first round
        self.attacker, self.defender = self.round_manager.initialize_round(
            self.attacker, self.defender, self.deck)
            
        # Original code creates board_manager here, keeping for consistency
        self.board_manager = BoardManager(trump_card=self.trump_card)

        # Main game loop
        while not self.rules_manager.is_game_over(len(self.deck), *self.players):
            self.__setup_round()
            
            # Play the round - exit if game is over
            if not self.__play_round():
                break

        logger.info("Game has ended.")

    def update_roles(self, switch_roles=False):
        """
        Update the roles of attacker and defender if needed
        
        Args:
            switch_roles (bool): Whether to switch attacker and defender roles
        """
        if switch_roles:
            logger.info("Switching roles: attacker becomes defender, defender becomes attacker")
            self.attacker, self.defender = self.defender, self.attacker
            
            # Update turn manager with new attacker/defender
            if hasattr(self, 'turn_manager') and self.turn_manager:
                self.turn_manager.set_players(self.attacker, self.defender)
            
            logger.info(f"New attacker: {self.attacker.name}, " +
                        f"New defender: {self.defender.name}")
        else:
            logger.info(f"Roles remain the same. Attacker: " +
                        f"{self.attacker.name}, Defender: " + 
                        f"{self.defender.name}")
