"""
Unit tests for the RoundManager class in the Durak game.

This module contains various tests to ensure that the RoundManager class is
working as expected. It includes tests to check if a round can be initialized,
if roles can be switched, if cards can be dealt to players, and if a real game
scenario can be simulated with multiple rounds.
"""


import logging
import unittest
from game_logic.card_package import Card, Suit, Rank, Deck
from game_logic.players import Player
from game_logic.game_management import DeckManager, PlayerManager, RulesManager
from game_logic.game_management import RoundManager

logger = logging.getLogger(__name__)


class TestRoundManager(unittest.TestCase):

    def setUp(self):
        """
        Set up the RoundManager with two players and a deck.
        """

        # Players setup
        self.attacker = Player(name="Alice")
        self.defender = Player(name="Bob")

        # Deck setup
        self.deck = Deck()

        # Rewrite self.deck to make it have only Aces, Kings, Queens and Jacks
        ranks = [Rank.TEN]
        suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS]
        cards = [Card(suit, rank) for suit in suits for rank in ranks]
        trump_card = Card(Suit.SPADES, Rank.TEN)

        self.deck.set_custom_deck(cards)
        self.deck.set_custom_trump_card(trump_card)

        logger.info(f"Current trump card: {self.deck.trump_card}")
        logger.info("Dealing cards to players...\n\n")

        # Set player names
        self.attacker.name = "Alice"
        self.defender.name = "Bob"

        # Set hands
        self.attacker.hand = [Card(Suit.SPADES, Rank.ACE),   # ♠️A
                              Card(Suit.SPADES, Rank.JACK),  # ♠️J
                              Card(Suit.CLUBS, Rank.KING),   # ♣️K
                              Card(Suit.CLUBS, Rank.QUEEN),  # ♣️Q
                              Card(Suit.CLUBS, Rank.JACK),   # ♣️J
                              Card(Suit.HEARTS, Rank.JACK)   # ♥️J
                              ]

        self.defender.hand = [Card(Suit.SPADES, Rank.KING),    # ♠️K
                              Card(Suit.DIAMONDS, Rank.ACE),   # ♦️A
                              Card(Suit.HEARTS, Rank.ACE),     # ♥️A
                              Card(Suit.DIAMONDS, Rank.KING),  # ♦️K
                              Card(Suit.HEARTS, Rank.QUEEN),   # ♥️Q
                              Card(Suit.DIAMONDS, Rank.QUEEN)  # ♦️Q
                              ]

    def test_initialize_round(self):
        """
        Test initializing a round, ensuring roles are assigned correctly and
        cards are dealt.
        """

        # Reset round number
        RoundManager.round_number = 0

        # Initialize the round
        attacker, defender = RoundManager.initialize_round(self.attacker,
                                                           self.defender,
                                                           self.deck)

        # Check round number
        self.assertEqual(RoundManager.round_number, 1)

        # Check if players have 6 cards each
        self.assertEqual(len(attacker.hand), 6)
        self.assertEqual(len(defender.hand), 6)

    def test_finalize_round_roles_switch(self):
        """
        Test finalizing a round with role switching.
        """
        RoundManager.finalize_round(roles_should_switch=True)
        self.assertTrue(RoundManager.roles_switched)

    def test_finalize_round_roles_remain(self):
        """
        Test finalizing a round without role switching.
        """
        RoundManager.finalize_round(roles_should_switch=False)
        self.assertFalse(RoundManager.roles_switched)

    def test_initialize_round_with_role_switch(self):
        """
        Test initializing a round with roles switching from the previous round.
        """

        # Finalize the previous round with role switch
        RoundManager.finalize_round(roles_should_switch=True)

        # Initialize the new round
        attacker, defender = RoundManager.initialize_round(self.attacker,
                                                           self.defender,
                                                           self.deck)

        # Check if roles have been switched
        self.assertEqual(attacker.name, "Bob")
        self.assertEqual(defender.name, "Alice")

        # Check if players have 6 cards each
        self.assertEqual(len(attacker.hand), 6)
        self.assertEqual(len(defender.hand), 6)

    def test_real_game_scenario_multiple_rounds(self):
        """
        Test a real game scenario with multiple rounds, role switching, and
        card dealing.
        """

        # Round 1 - Initial round
        attacker, defender = RoundManager.initialize_round(self.attacker,
                                                           self.defender,
                                                           self.deck)

        # Check if players have 6 cards each
        self.assertEqual(len(attacker.hand), 6)
        self.assertEqual(len(defender.hand), 6)

        # Simulate some game actions (e.g., playing cards)
        attacker.hand.pop()  # Attacker plays a card
        defender.hand.pop()  # Defender plays a card

        # Finalize round with role switch
        RoundManager.finalize_round(roles_should_switch=True)

        # Round 2 - Roles should switch
        attacker, defender = RoundManager.initialize_round(attacker, defender,
                                                           self.deck)

        # Check if roles have been switched
        self.assertEqual(attacker.name, "Bob")
        self.assertEqual(defender.name, "Alice")

        # Check if players have 5 cards each
        self.assertEqual(len(attacker.hand), 5)
        self.assertEqual(len(defender.hand), 5)

        # Simulate more game actions
        attacker.hand.pop()  # Attacker plays a card
        defender.hand.pop()  # Defender plays a card

        # Finalize round without role switch
        RoundManager.finalize_round(roles_should_switch=False)

        # Round 3 - Roles should remain the same
        attacker, defender = RoundManager.initialize_round(attacker, defender,
                                                           self.deck)

        # Check if roles remain the same
        self.assertEqual(attacker.name, "Bob")
        self.assertEqual(defender.name, "Alice")

        # Check if players have 4 cards each
        self.assertEqual(len(attacker.hand), 4)
        self.assertEqual(len(defender.hand), 4)

    def test_end_game_scenario(self):
        """
        Test simulating an end of game scenario where the deck is empty and
        players have no cards.
        """

        # Initialize the round
        attacker, defender = RoundManager.initialize_round(self.attacker,
                                                           self.defender,
                                                           self.deck)

        # Simulate end of game scenario
        while len(self.deck) > 0 or (attacker.has_cards() and defender.has_cards()):

            # Initialize the round
            if RoundManager.round_number != 1:
                attacker, defender = RoundManager.initialize_round(attacker,
                                                                     defender,
                                                                   self.deck)

            logger.info("--------------------------------------------------")
            logger.info(f"Round {RoundManager.round_number}")
            logger.info("--------------------------------------------------\n")

            logger.info(f"Deck: {self.deck}\n")
            logger.info(f"Attacker: {attacker.hand}")
            logger.info(f"Defender: {defender.hand}\n")

            attacker.hand.pop()  # Attacker plays a card
            defender.hand.pop()  # Defender plays a card

            logger.info("Players have played their cards.\n")

            # Players draw cards
            logger.info(f"Attacker: {attacker.hand}")
            logger.info(f"Defender: {defender.hand}\n")

            # Check if the trump card has been drawn
            trump_card_drawn = self.deck.trump_card is not None
            deck_size = len(self.deck) + int(trump_card_drawn)
            logger.info(f"Deck size: {deck_size}")

            card_distribution = RulesManager.determine_card_distribution(
                deck_size, attacker, defender)

            logger.info(f"Card distribution: {card_distribution}")

            for _ in range(card_distribution['attacker']):
                if DeckManager.can_draw_card_to_player(self.deck):
                    card = DeckManager.draw_card(self.deck)
                    logger.info(f"Dealt {card} to {attacker.name}")
                    PlayerManager.add_card_to_hand(attacker, card)
                elif DeckManager.get_trump_card(self.deck):
                    card = DeckManager.draw_trump_card(self.deck)
                    logger.info(f"Dealt {card} to {attacker.name}")
                    PlayerManager.add_card_to_hand(attacker, card)
                else:
                    logger.warning("Deck is empty; cannot deal more cards.")
                    break

            for _ in range(card_distribution['defender']):
                if DeckManager.can_draw_card_to_player(self.deck):
                    card = DeckManager.draw_card(self.deck)
                    logger.info(f"Dealt {card} to {defender.name}")
                    PlayerManager.add_card_to_hand(defender, card)
                elif DeckManager.get_trump_card(self.deck):
                    card = DeckManager.draw_trump_card(self.deck)
                    logger.info(f"Dealt {card} to {defender.name}")
                    PlayerManager.add_card_to_hand(defender, card)
                else:
                    logger.warning("Deck is empty; cannot deal more cards.")
                    break

            RoundManager.finalize_round(roles_should_switch=True)

            if RoundManager.round_number == 1:
                RoundManager.round_number += 1

        # Ensure the game ends when the deck is empty
        self.assertTrue(self.deck.is_empty())
        self.assertFalse(attacker.has_cards() or defender.has_cards())


if __name__ == '__main__':
    unittest.main()
