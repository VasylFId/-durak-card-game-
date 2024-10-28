import logging
import unittest
from game_logic.card_package import Card, Suit, Rank, Deck
from game_logic.players import Player
from game_logic.game_management import PlayerManager, DeckManager, RoundManager, RulesManager, TrumpManager

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
        
        # Rewrite self.deck to make it have only Aces, Kings and Queens:
        ranks = [Rank.ACE, Rank.KING, Rank.QUEEN]
        suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        cards = [Card(suit, rank) for suit in suits for rank in ranks]
        cards += [Card(Suit.DIAMONDS, Rank.JACK)]  # Add a Jack to the deck
        cards += [Card(Suit.HEARTS, Rank.JACK)]  # Add a Jack to the deck
        cards += [Card(Suit.CLUBS, Rank.JACK)] 
        cards += [Card(Suit.SPADES, Rank.JACK)] 
    
        logger.info(f"Custom deck: {cards}")    
        self.deck.set_custom_deck(cards)

        logger.info(f"Current trump card: {self.deck.trump_card}")
        
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

    def test_end_game_scenario(self):
        """
        Test simulating an end of game scenario where the deck is empty and players have no cards.
        """

        print(self.deck)

        logger.info("Dealing cards to players...")

        players = [self.attacker, self.defender]

        # Deal initial cards to players

        for player in players:
            while not PlayerManager.player_has_enough_cards(player, hand_size=6) and DeckManager.can_draw_card_to_player(self.deck):
                card = DeckManager.draw_card(self.deck)
                PlayerManager.add_card_to_hand(player, card)
                logger.info(f"Dealt {card} to {player.name}")


        trump_card = DeckManager.get_trump_card(self.deck)

        while not TrumpManager.is_trump_card_valid(self.deck, players):
            DeckManager.reset_trump_card(self.deck)
            trump_card = DeckManager.get_trump_card(self.deck)
        
        for player in players:
            PlayerManager.set_player_trump_suit(player, trump_card)

        DeckManager.show_remaining_cards_number(self.deck)
        logger.info("Dealing cards complete.")
        
        # get trump card from deck
        trump_card = DeckManager.get_trump_card(self.deck)
        logger.info(f"Trump card: {trump_card}")
        
        if not TrumpManager.is_trump_card_valid(self.deck, players):
            TrumpManager.set_new_trump_card(self.deck, players)


        # Check who has the lowest trump card
        trump_card = DeckManager.get_trump_card(self.deck)
        attacking_player = PlayerManager.get_lowest_trump_card_player(players, trump_card)

        # Set the attacking player
        self.attacker = attacking_player
        self.defender = [player for player in players if player != attacking_player][0]

        print(self.deck)

        attacker, defender = RoundManager.initialize_round(self.attacker, self.defender, self.deck)

        # Simulate end of game scenario
        while len(self.deck) > 0 or (attacker.has_cards() or defender.has_cards()):
            logger.info(f"Deck: {self.deck}")
            logger.info(f"Attacker: {attacker.hand}")
            logger.info(f"Defender: {defender.hand}")
            
            attacker.hand.pop()  # Attacker plays a card
            defender.hand.pop()  # Defender plays a card

            card_distribution = RulesManager.determine_card_distribution(len(self.deck), attacker, defender)

            for _ in range(card_distribution['attacker']):
                if DeckManager.can_draw_card_to_player(self.deck):
                    card = DeckManager.draw_card(self.deck)
                    PlayerManager.add_card_to_hand(attacker, card)
                    logger.info(f"Dealt {card} to {attacker.name}")
                else:
                    logger.warning("Deck is empty; cannot deal more cards.")
                    break

            for _ in range(card_distribution['defender']):
                if DeckManager.can_draw_card_to_player(self.deck):
                    card = DeckManager.draw_card(self.deck)
                    PlayerManager.add_card_to_hand(defender, card)
                    logger.info(f"Dealt {card} to {defender.name}")
                else:
                    logger.warning("Deck is empty; cannot deal more cards.")
                    break
        
        # # Ensure the game ends when the deck is empty
        self.assertTrue(self.deck.is_empty())
        self.assertFalse(attacker.has_cards() or defender.has_cards())


if __name__ == '__main__':
    unittest.main()
