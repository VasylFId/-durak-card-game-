from game_logic.cards import Suit, Rank, Card, Deck, DeckManager
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_cards_module():
    # Create some cards
    card1 = Card(Suit.CLUBS, Rank.QUEEN)
    card2 = Card(Suit.HEARTS, Rank.JACK)
    card3 = Card(Suit.DIAMONDS, Rank.KING)
    card4 = Card(Suit.CLUBS, Rank.ACE)
    card5 = Card(Suit.SPADES, Rank.KING)
    card6 = Card(Suit.SPADES, Rank.ACE)
    trump_suit = Suit.CLUBS

    # Compare cards with various scenarios
    logger.info(f"Comparing {card1} with {card2} (Trump: {trump_suit}) -> {card1.compare(card2, trump_suit)}")
    logger.info(f"Comparing {card2} with {card3} (Trump: {trump_suit}) -> {card2.compare(card3, trump_suit)}")
    logger.info(f"Comparing {card3} with {card5} (Trump: {trump_suit}) -> {card3.compare(card5, trump_suit)}")
    logger.info(f"Comparing {card4} with {card1} (Trump: {trump_suit}) -> {card4.compare(card1, trump_suit)}")
    logger.info(f"Comparing {card2} with {card3} (Trump: {trump_suit}) -> {card2.compare(card3, trump_suit)}")
    logger.info(f"Comparing {card5} with {card4} (Trump: {trump_suit}) -> {card5.compare(card4, trump_suit)}")
    logger.info(f"Comparing {card2} with {card1} (Trump: {trump_suit}) -> {card2.compare(card1, trump_suit)}")
    logger.info(f"Comparing {card3} with {card1} (Trump: {trump_suit}) -> {card3.compare(card1, trump_suit)}")
    logger.info(f"Comparing {card4} with {card2} (Trump: {trump_suit}) -> {card4.compare(card2, trump_suit)}")
    logger.info(f"Comparing {card5} with {card2} (Trump: {trump_suit}) -> {card5.compare(card2, trump_suit)}")

    # Additional edge cases for comparison
    trump_card = Card(Suit.CLUBS, Rank.TEN)
    non_trump_card = Card(Suit.HEARTS, Rank.TEN)
    logger.info(f"Comparing trump {trump_card} with non-trump {non_trump_card} -> {trump_card.compare(non_trump_card, trump_suit)}")
    
    non_trump_card2 = Card(Suit.DIAMONDS, Rank.NINE)
    logger.info(f"Comparing non-trump {non_trump_card} with non-trump {non_trump_card2} -> {non_trump_card.compare(non_trump_card2, trump_suit)}")
    
    trump_card2 = Card(Suit.CLUBS, Rank.SIX)
    logger.info(f"Comparing trump {trump_card} with trump {trump_card2} -> {trump_card.compare(trump_card2, trump_suit)}")

    # Test Deck and DeckManager
    deck = Deck()
    deck_manager = DeckManager(deck)

    # Initial trump card
    trump_card = deck.draw_trump_card()
    logger.info(f"Initial Trump Card: {trump_card}")

    # Drawing cards for players and sorting hands
    alice_hand = [deck.draw_card() for _ in range(6)]
    bob_hand = [deck.draw_card() for _ in range(6)]
    logger.info(f"Alice's hand: {', '.join(map(str, alice_hand))}")
    logger.info(f"Bob's hand: {', '.join(map(str, bob_hand))}")

    # Sort hands based on trump suit
    alice_hand.sort(key=lambda card: (card.is_trump(trump_suit), card.weight), reverse=True)
    bob_hand.sort(key=lambda card: (card.is_trump(trump_suit), card.weight), reverse=True)
    logger.info(f"Alice's sorted hand: {', '.join(map(str, alice_hand))}")
    logger.info(f"Bob's sorted hand: {', '.join(map(str, bob_hand))}")

    # Drawing a card and handling empty deck
    try:
        drawn_card = deck.draw_card()
        logger.info(f"Card drawn: {drawn_card}")
        deck.return_card(drawn_card)
        deck.shuffle()
    except ValueError as e:
        logger.error(e)

    # Attempt to draw from empty deck
    try:
        while True:
            deck.draw_card()
    except ValueError as e:
        logger.info(f"Expected error when drawing from empty deck: {e}")

# Run the tests
if __name__ == "__main__":
    test_cards_module()
