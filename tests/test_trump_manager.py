import logging
import unittest
from game_logic.game_management import DeckManager, TrumpManager
from game_logic.card_package import Deck, Card, Suit, Rank
from game_logic.players import Player

# Setup logging before any tests
logger = logging.getLogger(__name__)


class TestTrumpManager(unittest.TestCase):
    def setUp(self):
        """
        Initialize DeckManager, TrumpManager, and Player instances for each test.
        Remove assigned cards from the deck.
        """
        self.deck = Deck()
        self.deck.return_card(self.deck.trump_card)
        self.deck_Deck_trump_card = None

        self.deck_manager = DeckManager()
        self.player1 = Player(name="Alice")
        self.player2 = Player(name="Bob")
        self.players = [self.player1, self.player2]

        # Predefine the cards and assign them to the players
        self.player1.hand = [
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.QUEEN)
        ]

        # [♦️A, ♣️A, ♣️K, ♥️K, ♦️Q, ♣️Q]

        self.player2.hand = [
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.JACK),
            Card(Suit.CLUBS, Rank.TEN),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.DIAMONDS, Rank.JACK),
            Card(Suit.CLUBS, Rank.NINE)
        ]

        # [♦️K, ♣️J, ♣️10, ♥️Q, ♦️J, ♣️9]

        # Remove these cards from the deck if they exist
        print("Initial deck:", self.deck._Deck__cards)

        for player in self.players:
            for card in player.hand:
                if card in self.deck:
                    self.deck._Deck__cards.remove(card)

        self.deck.set_trump_card()

        print("Deck after removing assigned cards:", self.deck)

    def test_trump_card_is_ace(self):
        """
        Test the private method __trump_card_is_ace.
        """
        ace_of_spades = Card(Suit.SPADES, Rank.ACE) # ♠️A
        self.assertTrue(TrumpManager._TrumpManager__trump_card_is_ace(ace_of_spades))
        non_ace = Card(Suit.HEARTS, Rank.KING) # ♥️K
        self.assertFalse(TrumpManager._TrumpManager__trump_card_is_ace(non_ace))

    def test_players_have_trump(self):
        """
        Test the private method __players_have_trump.
        """
        trump_card = Card(Suit.SPADES, Rank.TEN) # ♠️10

        # Test when no player has a trump card
        self.assertFalse(TrumpManager._TrumpManager__players_have_trump(self.players, trump_card))

        # Test when one player has a trump card
        self.player1.hand.append(trump_card)
        self.assertTrue(TrumpManager._TrumpManager__players_have_trump(self.players, trump_card))

        # Test when both players have a trump card
        self.player2.hand.append(trump_card)
        self.assertTrue(TrumpManager._TrumpManager__players_have_trump(self.players, trump_card))

    def test_is_trump_card_valid(self):
        """
        Test the public method is_trump_card_valid.
        """
        trump_card = Card(Suit.SPADES, Rank.ACE) # ♠️A

        self.deck._Deck__trump_card = trump_card

        if trump_card in self.deck:
            self.deck._Deck__cards.remove(trump_card)

        # Test when the trump card is an Ace and no player has a trump card
        self.assertFalse(TrumpManager.is_trump_card_valid(self.deck, self.players))
        logger.info(self.deck)

        # Test when the trump card is an Ace and one player has a trump card
        self.player1.hand.append(trump_card)
        self.assertFalse(TrumpManager.is_trump_card_valid(self.deck, self.players))

        # Test when the trump card is an Ace and both players have a trump card
        self.player2.hand.append(trump_card)
        self.assertFalse(TrumpManager.is_trump_card_valid(self.deck, self.players))

        # Test when the trump card is not an Ace and no player has a trump card
        self.player1.hand.remove(trump_card)
        self.player2.hand.remove(trump_card)

        trump_card = Card(Suit.SPADES, Rank.TEN) # ♠️10

        self.deck.return_card(self.deck.trump_card)
        self.deck_Deck_trump_card = None
        self.deck._Deck__trump_card = trump_card

        self.assertFalse(TrumpManager.is_trump_card_valid(self.deck, self.players))

        # Test when the trump card is not an Ace and one player has a trump card
        self.player1.hand.append(trump_card)
        logger.info(self.player1.hand)
        logger.info(self.deck)
        self.assertTrue(TrumpManager.is_trump_card_valid(self.deck, self.players))

        # Test when the trump card is not an Ace and both players have a trump card
        self.player2.hand.append(trump_card)
        self.assertTrue(TrumpManager.is_trump_card_valid(self.deck, self.players))

    def test_set_new_trump_card(self):
        """
        Test the public method set_new_trump_card.
        """
        trump_card = Card(Suit.SPADES, Rank.ACE)  # ♠️A

        self.deck._Deck__trump_card = trump_card

        if trump_card in self.deck:
            self.deck._Deck__cards.remove(trump_card)

        logger.info("\n\nTest when the current trump card is an Ace:\n")
        # Test when the current trump card is an Ace
        new_trump_card = TrumpManager.set_new_trump_card(self.deck, self.players)
        self.assertNotEqual(trump_card, new_trump_card)
        self.assertEqual(new_trump_card, self.deck.trump_card)

        logger.info("\n\nTest when the current trump card is not an Ace:\n")
        # Test when the current trump card is not an Ace
        trump_card = Card(Suit.SPADES, Rank.TEN)  # ♠️10

        self.deck.return_card(self.deck.trump_card)
        self.deck_Deck_trump_card = None
        self.deck._Deck__trump_card = trump_card

        new_trump_card = TrumpManager.set_new_trump_card(self.deck, self.players)
        self.assertNotEqual(trump_card, new_trump_card)
        self.assertEqual(new_trump_card, self.deck.trump_card)


if __name__ == '__main__':
    unittest.main()
