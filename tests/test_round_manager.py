import logging
import unittest
from unittest.mock import MagicMock
from game_logic.card_package import Card, Suit, Rank, Deck
from game_logic.players import Player
from game_logic.game_management import PlayerManager, DeckManager, RoundManager

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
        
        # Mock deck to ensure consistent behavior
        self.deck.draw_card = MagicMock(side_effect=[
            Card(Suit.HEARTS, Rank.SIX),
            Card(Suit.SPADES, Rank.SEVEN),
            Card(Suit.DIAMONDS, Rank.EIGHT),
            Card(Suit.CLUBS, Rank.NINE),
            Card(Suit.HEARTS, Rank.TEN),
            Card(Suit.SPADES, Rank.JACK),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.SPADES, Rank.SIX),
            Card(Suit.DIAMONDS, Rank.SEVEN),
            Card(Suit.CLUBS, Rank.EIGHT),
            Card(Suit.HEARTS, Rank.NINE),
            Card(Suit.SPADES, Rank.TEN),
            Card(Suit.DIAMONDS, Rank.JACK),
            Card(Suit.CLUBS, Rank.QUEEN),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.SIX),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.HEARTS, Rank.EIGHT),
            Card(Suit.SPADES, Rank.NINE),
            Card(Suit.DIAMONDS, Rank.TEN),
            Card(Suit.CLUBS, Rank.JACK),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.DIAMONDS, Rank.ACE),
            # Add more cards here to prevent StopIteration
            Card(Suit.CLUBS, Rank.SIX),
            Card(Suit.HEARTS, Rank.SEVEN),
            Card(Suit.SPADES, Rank.EIGHT),
            Card(Suit.DIAMONDS, Rank.NINE),
            Card(Suit.CLUBS, Rank.TEN),
            Card(Suit.HEARTS, Rank.JACK),
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.ACE),
        ])

    def test_initialize_round(self):
        """
        Test initializing a round, ensuring roles are assigned correctly and cards are dealt.
        """
        attacker, defender = RoundManager.initialize_round(self.attacker, self.defender, self.deck)
        
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

    def test_deal_cards(self):
        """
        Test dealing cards to players to ensure they have enough cards.
        """
        # Remove all cards from players' hands to simulate end of round
        self.attacker.hand = []
        self.defender.hand = []
        
        # Deal cards
        RoundManager.deal_cards(self.attacker, self.defender, self.deck)
        
        # Check if players have 6 cards each
        self.assertEqual(len(self.attacker.hand), 6)
        self.assertEqual(len(self.defender.hand), 6)

    def test_initialize_round_with_role_switch(self):
        """
        Test initializing a round with roles switching from the previous round.
        """
        # Finalize the previous round with role switch
        RoundManager.finalize_round(roles_should_switch=True)
        
        # Initialize the new round
        attacker, defender = RoundManager.initialize_round(self.attacker, self.defender, self.deck)
        
        # Check if roles have been switched
        self.assertEqual(attacker.name, "Bob")
        self.assertEqual(defender.name, "Alice")
        
        # Check if players have 6 cards each
        self.assertEqual(len(attacker.hand), 6)
        self.assertEqual(len(defender.hand), 6)

    def test_real_game_scenario_multiple_rounds(self):
        """
        Test a real game scenario with multiple rounds, role switching, and card dealing.
        """
        # Round 1 - Initial round
        attacker, defender = RoundManager.initialize_round(self.attacker, self.defender, self.deck)
        
        # Check if players have 6 cards each
        self.assertEqual(len(attacker.hand), 6)
        self.assertEqual(len(defender.hand), 6)
        
        # Simulate some game actions (e.g., playing cards)
        attacker.hand.pop()  # Attacker plays a card
        defender.hand.pop()  # Defender plays a card
        
        # Finalize round with role switch
        RoundManager.finalize_round(roles_should_switch=True)
        
        # Round 2 - Roles should switch
        attacker, defender = RoundManager.initialize_round(attacker, defender, self.deck)
        
        # Check if roles have been switched
        self.assertEqual(attacker.name, "Bob")
        self.assertEqual(defender.name, "Alice")
        
        # Check if players have 6 cards each
        self.assertEqual(len(attacker.hand), 6)
        self.assertEqual(len(defender.hand), 6)
        
        # Simulate more game actions
        attacker.hand.pop()  # Attacker plays a card
        defender.hand.pop()  # Defender plays a card
        
        # Finalize round without role switch
        RoundManager.finalize_round(roles_should_switch=False)
        
        # Round 3 - Roles should remain the same
        attacker, defender = RoundManager.initialize_round(attacker, defender, self.deck)
        
        # Check if roles remain the same
        self.assertEqual(attacker.name, "Bob")
        self.assertEqual(defender.name, "Alice")
        
        # Check if players have 6 cards each
        self.assertEqual(len(attacker.hand), 6)
        self.assertEqual(len(defender.hand), 6)
        
        # Simulate end of game scenario
        while len(self.deck) > 0 and (attacker.has_cards() or defender.has_cards()):
            logger.info(f"Deck: {self.deck}")
            logger.info(f"Attacker: {attacker.hand}")
            logger.info(f"Defender: {defender.hand}")
            
            attacker.hand.pop()  # Attacker plays a card
            defender.hand.pop()  # Defender plays a card

            logger.info(f"Deck: {self.deck}")
            logger.info(f"Attacker: {attacker.hand}")
            logger.info(f"Defender: {defender.hand}")

            RoundManager.deal_cards(attacker, defender, self.deck)

            logger.info(f"Deck: {self.deck}")
            logger.info(f"Attacker: {attacker.hand}")
            logger.info(f"Defender: {defender.hand}")
        
        # # Ensure the game ends when the deck is empty
        # self.assertTrue(self.deck.is_empty())
        # self.assertFalse(attacker.has_cards() or defender.has_cards())


if __name__ == '__main__':
    unittest.main()
