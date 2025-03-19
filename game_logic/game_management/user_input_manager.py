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
            if valid_responses is None or response in valid_responses:
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

        # Get the player's hand (reversed to prefer lower cards first)
        player_hand = PlayerManager.get_player_hand(player)
        
        # If using for AI, sort by non-trump first, then by weight
        sorted_hand = sorted(
            player_hand, 
            key=lambda card: (card.is_trump(board_manager.trump_card.suit), card.weight)
        )
        
        # Empty board - any card is valid for attack
        if not board_manager.get_board_state():
            if sorted_hand:
                suggested_card = sorted_hand[0]  # Get lowest non-trump card
                logger.info(f"Suggested card for attack (empty board): {suggested_card}")
                return suggested_card
            return None
            
        # Get ranks already on the board
        board_ranks = board_manager.get_board_ranks()
        
        # Find all cards with matching ranks
        valid_cards = [card for card in sorted_hand if card.rank in board_ranks]
        
        if valid_cards:
            suggested_card = valid_cards[0]  # Get the first (lowest) valid card
            logger.info(f"Suggested card for attack (matching rank): {suggested_card}")
            return suggested_card
            
        logger.info("No valid card found for attack")
        return None

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

        # Get the player's hand
        player_hand = PlayerManager.get_player_hand(player)
        valid_defenses = []
        
        # Find all cards that can legally defend against the attack
        for card in player_hand:
            # Same suit, higher rank
            if card.suit == attacking_card.suit and card.weight > attacking_card.weight:
                valid_defenses.append(card)
            # Trump vs non-trump
            elif (card.is_trump(board_manager.trump_card.suit) and 
                  not attacking_card.is_trump(board_manager.trump_card.suit)):
                valid_defenses.append(card)
        
        # If we have valid defenses, return the lowest one
        if valid_defenses:
            suggested_card = min(valid_defenses, key=lambda c: c.weight)
            logger.info(f"Suggested card for defense: {suggested_card}")
            return suggested_card
            
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
        
        # For AI players, we don't need to print the hand or get input
        is_ai_player = player_name.startswith("AI_")
        
        # If not AI, print the player's hand
        if not is_ai_player:
            print(f"{player_name}, your hand: {hand}")
            
        # Determine the context and prompt the player accordingly
        if context == "attack":
            suggested_card = self.__get_suggested_card_to_attack(board_manager, player)

            # If there's no suggested card, let the player choose
            if not suggested_card:
                return None
                
            # If AI, automatically use the suggested card
            if is_ai_player:
                # AI automatically uses the suggested card
                logger.info(f"AI using suggested attack card: {suggested_card}")
                return PlayerManager.select_card(player, suggested_card)
                
            # Prompt the player to use the suggested card
            logger.info(f"Suggested card to attack: {suggested_card}")

            # Get the player's choice
            use_suggested = self.get_input(
                f"Do you want to use the suggested card ({suggested_card})?" +
                "(y/n/skip): ",
                ["y", "n", "skip"]
            )

            # If the player chooses to use the suggested card, return it
            logger.info(f"Attack Player's choice: {use_suggested}")

            # If the player chooses to use the suggested card, return it
            if use_suggested == "y":
                return PlayerManager.select_card(player, suggested_card)
            elif use_suggested == "skip":
                return None
            
            # If the player chooses not to use the suggested card, let them choose
            return self._show_hand_and_prompt(player, hand)
            
        # If the context is defense, prompt the player to select a card to defend
        elif context == "defense":

            # Check if there's an attacking card to defend against
            if attacking_card:
                suggested_card = self.__get_suggested_card_to_defend(
                    board_manager, player, attacking_card)
                    
                # If there's no suggested card, let the player choose
                if not suggested_card:
                    return None
                
                # If AI, automatically use the suggested card
                if is_ai_player:
                    # AI automatically uses the suggested card
                    logger.info(f"AI using suggested defense card: {suggested_card}")
                    return PlayerManager.select_card(player, suggested_card)
                
                # Prompt the player to use the suggested card
                logger.info(f"Suggested card to defend: {suggested_card}")
                use_suggested = self.get_input(
                    f"Suggested card to defend: {suggested_card}. " +
                    "Do you want to use it? (y/n/fail): ",
                    ["y", "n", "fail"]
                )

                # If the player chooses to use the suggested card, return it
                logger.info(f"Defence Player's choice: {use_suggested}")
                if use_suggested == "y":
                    return PlayerManager.select_card(player, suggested_card)
                elif use_suggested == "fail":
                    return None
                
                # If the player chooses not to use the suggested card, let them choose
                logger.info(f"Attacking card: {attacking_card}")
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
