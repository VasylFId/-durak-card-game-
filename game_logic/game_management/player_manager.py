import logging
from game_logic.card_package import Deck, Card
from game_logic.players import Player
from game_logic.game_management import DeckManager

logger = logging.getLogger(__name__)


class PlayerManager:
    @staticmethod
    def player_has_enough_cards(player: Player, hand_size: int = 6):
        """
        Checks if a player has enough cards in their hand.

        Args:
            player (Player): The player to check.
            hand_size (int): The minimum number of cards required.

        Returns:
            bool: True if the player has enough cards, False otherwise.
        """
        logger.info(f"Checking if {player.name} has enough cards...")
        logger.info(f"{player.name} has {len(player.hand)} cards")
        return len(player.hand) >= hand_size

    @staticmethod
    def deal_initial_cards(deck: Deck, player: Player, hand_size: int = 6):
        """
        Deals the initial cards to a player.

        Args:
            deck (Deck): The deck of cards to draw from.
            player (Player): The player to deal cards to.
            hand_size (int): The number of cards to deal.
        """

        logger.info(f"Dealing initial cards to {player.name}...")
        while not PlayerManager.player_has_enough_cards(player, hand_size):
            card_to_draw = DeckManager.draw_card(deck)
            PlayerManager.add_card_to_hand(player, card_to_draw)

    @staticmethod
    def add_card_to_hand(player: Player, card: Card) -> None:
        """
        Adds a card to a player's hand.

        Args:
            player (Player): The player to add the card to.
            card (Card): The card to add.
        """
        player.add_card_to_hand(card)

    @staticmethod
    def remove_card_from_hand(player: Player, card: Card):
        """
        Removes a specified card from the player's hand.

        Args:
            player (Player): The player from whose hand to remove the card.
            card (Card): The card to be removed.

        Raises:
            ValueError: If the card is not found in the player's hand.
        """
        if player.remove_card_from_hand(card):
            logger.info(f"Removed {card} from {player.name}'s hand.")
        else:
            raise ValueError(f"{card} not found in {player.name}'s hand.")

    @staticmethod
    def pick_up_card(player: Player, card: Card):
        """
        Adds a specified card to the player's hand.

        Args:
            player (Player): The player who is picking up the card.
            card (Card): The card to be added to the player's hand.
        """
        player.hand.append(card)
        logger.info(f"{player.name} picked up {card}.")

    @staticmethod
    def select_card(player: Player, card: Card) -> Card:
        """
        Selects a card from the player's hand.

        Args:
            player (Player): The player selecting the card.
            card (Card): The card to be selected.

        Returns:
            Card: The selected card.

        Raises:
            ValueError: If the card is not found in the player's hand.
        """
        if card in player.hand:
            logger.info(f"{player.name} selected {card}.")
            return card
        else:
            raise ValueError(f"{card} not found in {player.name}'s hand.")

    @staticmethod
    def get_player_hand(player: Player) -> list:
        """
        Returns the player's current hand.

        Args:
            player (Player): The player to get the hand from.

        Returns:
            list: The sorted hand of the player.
        """
        logger.info(f"Getting {player.name}'s hand...")
        logger.info(f"{player.name} has {player.hand}")
        return player.hand

    @staticmethod
    def get_player_name(player: Player) -> str:
        """
        Returns the player's name.

        Args:
            player (Player): The player to get the name from.

        Returns:
            str: The name of the player.
        """
        return player.name

    @staticmethod
    def get_player_trump_suit(player: Player) -> str:
        """
        Returns the player's trump suit.

        Args:
            player (Player): The player to get the trump suit from.

        Returns:
            str: The trump suit of the player.
        """
        return player.trump_suit

    @staticmethod
    def set_player_trump_suit(player: Player, trump_card: Card) -> None:
        """
        Sets the player's trump suit.

        Args:
            player (Player): The player to set the trump suit for.
            trump_card (Card): The card to set the trump suit from.
        """
        player.update_trump_suit(trump_card.suit)
        logger.info(f"{player.name} set trump suit to {trump_card.suit}")

    @staticmethod
    def get_player_card_count(player: Player) -> int:
        """
        Returns the number of cards in the player's hand.

        Args:
            player (Player): The player to get the card count from.

        Returns:
            int: The number of cards in the player's hand.
        """
        return len(player.hand)
