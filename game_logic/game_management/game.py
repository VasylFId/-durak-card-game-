import logging
from .player import Player
from .ai import AIPlayer
from .cards import Deck, Card, Suit, Rank

logger = logging.getLogger(__name__)

class DurakGame:
    def __init__(self):
        self.players = []
        self.trump_suit = None
        self.active_player_index = 0
        self.table_cards = []
        self.deck = Deck()
        self.starting_player = None
        self.round_number = 1
        self.round_manager = RoundManager(self)
        self.turn_manager = TurnManager(self)
        self.card_manager = CardManager(self)

    def add_player(self, player: Player):
        self.players.append(player)

    def start_game(self):
        self._initialize_game()
        self.round_manager.start_round()

    def _initialize_game(self):
        self.deck.shuffle()
        self._set_trump_card()
        self._deal_initial_cards()
        self._determine_starting_player()

    def _set_trump_card(self):
        self.trump_card = self.card_manager.draw_trump_card(self.deck)
        self.trump_suit = self.trump_card.suit
        logger.info(f"Trump card: {self.trump_card}, Trump suit: {self.trump_suit}")
        logger.info("-" * 40)  # Separator line

    def _deal_initial_cards(self):
        self.card_manager.deal_initial_hands(self.players, self.deck, self.trump_suit)
        logger.info("-" * 40)  # Separator line

    def _determine_starting_player(self):
        self.starting_player = self.card_manager.find_starting_player(self.players, self.trump_suit)
        self.active_player_index = self.players.index(self.starting_player)
        logger.info(f"Starting player: {self.starting_player.name}")
        logger.info("-" * 40)  # Separator line

    def is_game_over(self) -> bool:
        return GameState.is_game_over(self)

    def get_winner(self) -> str:
        return GameState.get_winner(self) if self.is_game_over() else None

    def end_round(self, defender_picks_up: bool):
        # Clear the table cards
        self.card_manager.clear_table(self.table_cards)

        # Players pick up cards from the deck to ensure they have 6 cards
        for player in self.players:
            while len(player.hand) < 6 and self.deck.cards:
                player.hand.append(self.deck.draw_card())
            player.sort_hand(self.trump_suit)  # Sort hand after drawing cards

        logger.info("-" * 40)  # Separator line
        logger.info(f"Round {self.round_number} ended.")
        print(f"Round {self.round_number} ended.")

        if defender_picks_up:
            # The attacker remains the same, and the defender becomes the new attacker
            pass
        else:
            # The defender successfully defended, so roles switch as usual
            self.active_player_index = (self.active_player_index + 1) % len(self.players)

        # Increment the round number after logging the end of the previous round
        self.round_number += 1
        logger.info(f"Round {self.round_number} begins.")
        print(f"Round {self.round_number} begins.")

        # Log new hands after round ends
        for player in self.players:
            logger.info(f"{player.name}'s new hand: {player.show_hand()}")
            logger.info("-" * 40)  # Separator line

    @property
    def current_player(self) -> Player:
        # Derive the current player based on the active_player_index
        return self.players[self.active_player_index]

    def defend(self, defender: Player, attack_card: Card, defense_card: Card) -> bool:
        """
        Determine if the defense is valid. 
        A valid defense occurs when the defense card is of the same suit and higher weight,
        or when the defense card is a trump card.
        """
        if defense_card.suit == attack_card.suit and defense_card.weight > attack_card.weight:
            return True
        elif defense_card.suit == self.trump_suit and attack_card.suit != self.trump_suit:
            return True
        else:
            logger.info(f"{defense_card} cannot beat {attack_card}")
            return False


class CardManager:
    def __init__(self, game: DurakGame):
        self.game = game

    def draw_trump_card(self, deck: Deck) -> Card:
        trump_card = deck.draw_trump_card()
        while trump_card.rank == Rank.ACE:
            logger.info("Trump card is Ace, redrawing...")
            deck.return_trump_card(trump_card)
            trump_card = deck.draw_trump_card()
        return trump_card

    def deal_initial_hands(self, players: list, deck: Deck, trump_suit: Suit):
        for player in players:
            player.draw_cards(deck, 6)
            player.sort_hand(trump_suit)
            logger.info(f"{player.name}'s hand: {player.show_hand()}")
            logger.info("-" * 40)  # Separator line
        self.ensure_trump_in_hands(players, deck, trump_suit)

    def ensure_trump_in_hands(self, players: list, deck: Deck, trump_suit: Suit):
        while not any(card.suit == trump_suit for player in players for card in player.hand):
            new_trump_card = self.draw_trump_card(deck)
            for player in players:
                player.sort_hand(trump_suit)
                logger.info(f"{player.name}'s hand after new trump: {player.show_hand()}")

    def find_starting_player(self, players: list, trump_suit: Suit) -> Player:
        lowest_trump_card = None
        starting_player = None
        for player in players:
            for card in player.hand:
                if card.suit == trump_suit and (lowest_trump_card is None or card < lowest_trump_card):
                    lowest_trump_card = card
                    starting_player = player
        return starting_player

    def clear_table(self, table_cards):
        """Clears the table cards."""
        table_cards.clear()
        logger.info("Table cards have been cleared.")
        logger.info("-" * 40)  # Separator line


class TurnManager:
    def __init__(self, game: DurakGame):
        self.game = game

    def play_turn(self):
        attacker = self.game.current_player
        defender = self._get_defender()

        logger.info(f"{attacker.name}'s turn to attack.")
        selected_card, action = PlayerInteraction.select_card(attacker, is_attacker=True)

        if action == "play" and selected_card:
            self._execute_attack(attacker, selected_card)
            self._handle_defense(defender)
        else:
            logger.info(f"{attacker.name} chose not to attack.")
            self.game.end_round(defender_picks_up=False)  # Attacker chose to end the round

    def _get_defender(self):
        return self.game.players[(self.game.active_player_index + 1) % len(self.game.players)]

    def _execute_attack(self, attacker: Player, card: Card):
        # Log the ranks of the cards on the table
        table_card_ranks = [c.rank for c in self.game.table_cards]
        logger.info(f"Table card ranks: {table_card_ranks}")

        # If there are cards on the table, enforce rank matching
        if self.game.table_cards:
            if not any(card.rank == table_card.rank for table_card in self.game.table_cards):
                logger.info(f"Cannot attack with {card}. Must use a card with rank matching those on the table.")
                return  # Prevents the attack if no cards match the rank on the table

        logger.info(f"{attacker.name} attacks with {card} of rank {card.rank}")
        attacker.play_card(card)  # Play the card (removes it from hand)
        self.game.table_cards.append(card)  # Add the card to the table
        attacker.sort_hand(self.game.trump_suit)

    def _handle_defense(self, defender: Player):
        while True:
            logger.info(f"{defender.name}'s turn to defend.")
            selected_card, action = PlayerInteraction.select_card(defender)

            if action == "defend":
                attack_card = self.game.table_cards[-1]  # The last card on the table is the attack card
                logger.info(f"Defender selected {selected_card} with rank {selected_card.rank} to defend against {attack_card} with rank {attack_card.rank}")
                
                if self.game.defend(defender, attack_card, selected_card):
                    logger.info(f"{defender.name} defended {attack_card} with {selected_card}")
                    self.game.table_cards.append(selected_card)
                    defender.hand.remove(selected_card)  # Remove the defending card from the defender's hand
                    defender.sort_hand(self.game.trump_suit)

                    # Check if the attacker can continue with the same rank
                    attacker = self.game.players[self.game.active_player_index]
                    if any(card.rank == selected_card.rank for card in attacker.hand):
                        logger.info("Attacker can continue with the same rank.")
                        selected_card, action = PlayerInteraction.select_card(attacker, is_attacker=True)
                        if action == "play":
                            logger.info(f"{attacker.name} played {selected_card} with rank {selected_card.rank}")
                            self.game.table_cards.append(selected_card)
                            attacker.play_card(selected_card)  # Ensure the card is removed from attacker's hand
                            attacker.sort_hand(self.game.trump_suit)
                        else:
                            break
                    else:
                        logger.info(f"{attacker.name} cannot continue attacking. Round ends.")
                        break
                else:
                    logger.info(f"Defense failed. Retry.")
                    continue  # Retry defense if the previous attempt was invalid
            elif action == "pickup":
                logger.info(f"{defender.name} picked up cards from the table.")
                defender.hand.extend(self.game.table_cards)
                defender.sort_hand(self.game.trump_suit)

                # End the current round, indicating that the defender picked up the cards
                self.game.end_round(defender_picks_up=True)
                return
            else:
                logger.info("Invalid action. Try again.")

class RoundManager:
    def __init__(self, game: DurakGame):
        self.game = game

    def start_round(self):
        if self.game.round_number > 1:  # Display "Round X continues" after the first round
            logger.info(f"Round {self.game.round_number} continues.")
        else:
            logger.info(f"Round {self.game.round_number} begins.")
        self.game.turn_manager.play_turn()
        self._finalize_round()

    def _finalize_round(self):
        # Ensure table clearing is done only once at the end of the round
        self.game.card_manager.clear_table(self.game.table_cards)
        # End the round by passing the control back to DurakGame
        if self.game.is_game_over():
            logger.info("Game over!")
            winner = self.game.get_winner()
            logger.info(f"The winner is {winner}.")
        else:
            self.game.round_manager.start_round()  # Start the next round if the game isn't over


class GameState:
    @staticmethod
    def is_game_over(game: DurakGame) -> bool:
        return (
            any(not player.has_cards() for player in game.players) or  # Check if any player has no cards left
            (not game.deck.cards and all(len(player.hand) < 6 for player in game.players))  # No cards left in the deck and all players have less than 6 cards
        )


    @staticmethod
    def get_winner(game: DurakGame) -> str:
        if GameState.is_game_over(game):
            for player in game.players:
                if len(player.hand) > 0:
                    return player.name
        return "Draw"  # If both players have no cards


class PlayerInteraction:
    @staticmethod
    def select_card(player: Player, is_attacker: bool = False) -> tuple:
        logger.info(f"{player.name}'s turn. Hand: {player.show_hand()}")
        while True:
            try:
                if is_attacker:
                    card_index = int(input(f"Select card (1-{len(player.hand)}) or 0 to cancel: ")) - 1
                    if card_index == -1:
                        return None, "cancel"
                    elif 0 <= card_index < len(player.hand):
                        selected_card = player.hand[card_index]
                        return selected_card, "play"
                else:
                    action = int(input("1. Defend\n2. Pick up\nSelect option: "))
                    if action == 2:
                        return None, "pickup"
                    elif action == 1:
                        card_index = int(input(f"Select card (1-{len(player.hand)}) or 0 to cancel: ")) - 1
                        if card_index == -1:
                            return None, "cancel"
                        elif 0 <= card_index < len(player.hand):
                            selected_card = player.hand[card_index]
                            return selected_card, "defend"
                logger.error("Invalid selection. Try again.")
            except ValueError:
                logger.error("Invalid input. Enter a number.")
