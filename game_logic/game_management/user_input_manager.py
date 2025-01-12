"""
This module contains the UserInputManager class, which is responsible for
handling user input during the game.

Classes:
    UserInputManager: A class for managing user input during the game.

Usage:
    user_input_manager = UserInputManager()
    card = user_input_manager.get_card_from_player(board_manager,
                                                   player,
                                                   context)
"""


import logging
from game_logic.players import Player
from game_logic.card_package import Card
from game_logic.game_management import BoardManager
from game_logic.game_management import PlayerManager, RulesManager

logger = logging.getLogger(__name__)


class UserInputManager:
    """
    A class for managing user input during the game.

    Methods:
        get_input(prompt, valid_responses):
            Gets input from the user and ensures it's a valid response if
            valid_responses is provided.
        get_card_from_player(board_manager, player, context, attacking_card):
            Prompts the player to select a card for either attacking or
            defending.
        _show_hand_and_prompt(player, hand):
            Helper method to show the player's hand and prompt them to select a
            card.
        __get_suggested_card_to_attack(board_manager, player):
            Suggests a card for the player to use in the current context.
        __get_suggested_card_to_defend(board_manager, player, attacking_card):
            Suggests a card for the player to use for defense.
    """

    @staticmethod
    def get_input(prompt: str, valid_responses: list = None) -> str:
        """
        Gets input from the user and ensures it's a valid response if
        valid_responses is provided.

        Args:
            prompt (str): The prompt to display to the user.
            valid_responses (list, optional): A list of valid responses.

        Returns:
            str: The user's input.
        """

        # If valid_responses is not provided, return the user's input as is
        # without validation
        while True:
            response = input(prompt).strip().lower()
            logger.info(f"User input: {response}")
            if response in valid_responses:
                logger.info(f"User input is valid: {response}")
                return response
            else:
                logger.info(f"User input is invalid: {response}")
                print("Invalid response. Please choose from: " +
                      f"{', '.join(valid_responses)}")

    def __get_suggested_card_to_attack(self, board_manager: BoardManager,
                                       player: Player) -> Card:
        """
        Suggests a card for the player to use in the current context.

        Args:
            player (Player): The player for whom to suggest a card.

        Returns:
            Card: The suggested card is the last card in the hand taken by
                  PlayerManager.
        """

        # Reverse the player's hand to suggest the last card first
        player_hand_reversed = PlayerManager.get_player_hand(player)[::-1]

        # If the board is empty, suggest the highest card in the player's hand
        if not board_manager.get_board_state():
            return player_hand_reversed[0]

        # Suggest the highest card that can be used for attack
        for card in player_hand_reversed:
            if RulesManager.is_valid_attack(board_manager, card):
                logger.info(f"Suggested card for attack: {card}")
                return card

    def __get_suggested_card_to_defend(self, board_manager, player: Player,
                                       attacking_card: Card) -> Card:
        """
        Suggests a card for the player to use for defense.

        Args:
            player (Player): The player who is defending.
            attacking_card (Card): The card that needs to be beaten.

        Returns:
            Card: The suggested card for defense, or None if no suitable card
            is found.
        """

        # Reverse the player's hand to suggest the last card first
        player_hand_reversed = PlayerManager.get_player_hand(player)[::-1]

        # Suggest the lowest card that can be used for defense
        for card in player_hand_reversed:
            if RulesManager.is_valid_defense(board_manager, attacking_card,
                                             card):
                logger.info(f"Suggested card for defense: {card}")
                return card

        logger.info("No suitable card found for defense.")

        return None

    def get_card_from_player(self, board_manager: BoardManager, player: Player,
                             context: str,
                             attacking_card: Card = None) -> Card:
        """
        Prompts the player to select a card for either attacking or defending.

        Args:
            player (Player): The player choosing the card.
            context (str): Either "attack" or "defense" to determine the prompt
            attacking_card (Card, optional): The card that needs to be beaten
                                            (for defense context).

        Returns:
            Card: The selected card.
        """

        # Get the player's name and hand
        player_name = PlayerManager.get_player_name(player)
        hand = PlayerManager.get_player_hand(player)

        # Check if the player has any cards in hand
        if not hand:
            raise ValueError("Player has no cards in hand.")

        logger.info(f"Prompting {player_name} to select a card for {context}.")
        print(f"{player_name}, your hand: {hand}")

        # If it's the attacker's turn
        if context == "attack":
            suggested_card = self.__get_suggested_card_to_attack(board_manager,
                                                                 player)

            if not suggested_card:
                return None

            print(f"Suggested card to attack: {suggested_card}")
            use_suggested = self.get_input(
                f"Do you want to use the suggested card ({suggested_card})?" +
                "(y/n/skip): ",
                ["y", "n", "skip"]
            )

            logger.info(f"Attack Player's choice: {use_suggested}")

            if use_suggested == "y":
                return PlayerManager.select_card(player, suggested_card)
            elif use_suggested == "skip":
                return None

            # If not using suggested card or no suggested card,
            # prompt for a different card
            return self._show_hand_and_prompt(player, hand)

        # If it's the defender's turn
        elif context == "defense":
            if attacking_card:
                suggested_card = self.__get_suggested_card_to_defend(
                    board_manager, player, attacking_card)

                if not suggested_card:
                    return None

                if suggested_card:
                    logger.info(f"Suggested card to defend: {suggested_card}")
                    use_suggested = self.get_input(
                        f"Suggested card to defend: {suggested_card}. " +
                        "Do you want to use it? (y/n/fail): ",
                        ["y", "n", "fail"]
                    )

                    logger.info(f"Defence Player's choice: {use_suggested}")

                    if use_suggested == "y":
                        return PlayerManager.select_card(player,
                                                         suggested_card)
                    elif use_suggested == "fail":
                        return None

            print(f"Attacking card: {attacking_card}")
            return self._show_hand_and_prompt(player, hand)

        else:
            raise ValueError(f"Invalid context: {context}. " +
                             "Must be 'attack' or 'defense'.")

    def _show_hand_and_prompt(self, player: Player, hand: list) -> Card:
        """
        Helper method to show the player's hand and prompt them to select a
        card.

        Args:
            player (Player): The player choosing the card.
            hand (list): The player's current hand.

        Returns:
            Card: The card selected by the player.
        """

        # Show the player's hand and prompt them to select a card
        card_numbers = {str(i + 1): card for i, card in enumerate(hand)}

        print(f"{PlayerManager.get_player_name(player)}, select a card:")

        # Print the card numbers and corresponding cards
        for number, card in card_numbers.items():
            print(f"{number}: {card}")

        # Get the player's choice
        choice = self.get_input(
            f"Select a card by entering the number (1-{len(hand)}): ",
            card_numbers.keys()
        )

        # Get the selected card based on the player's choice
        selected_card = card_numbers[choice]

        # Use PlayerManager to select the card from the player's hand
        return PlayerManager.select_card(player, selected_card)
