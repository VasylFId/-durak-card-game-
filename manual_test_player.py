from game_logic.cards import Deck, Suit, Card, Rank
from game_logic.player import Player
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_player_module():
    # Initialize deck and players
    deck = Deck()
    deck.shuffle()
    deck.set_trump_card()
    
    alice = Player("Alice")
    bob = Player("Bob")

    # Both players draw initial 6 cards
    alice.draw_card(deck, 6)
    bob.draw_card(deck, 6)

    # Check sorting
    logger.info(f"Alice's sorted hand: {alice.show_hand()}")
    logger.info(f"Bob's sorted hand: {bob.show_hand()}")

    # Alice attacks with the first card
    attack_card = alice.hand[0]
    alice_attack = alice.attack(attack_card)

    # Bob tries to defend with the first card
    bob_defense = bob.defend(attack_card, bob.hand[0])
    
    # If Bob failed, let him try another card
    if not bob_defense:
        logger.info(f"Bob failed to defend with {bob.hand[0]}, trying another card.")
        bob_defense = bob.defend(attack_card, bob.hand[1])

    # Attempt invalid attack with a card not in hand
    invalid_card = Card(Suit.SPADES, Rank.TEN)  # Using the correct Rank Enum
    alice_invalid_attack = alice.attack(invalid_card)

    # Attempt invalid defense with a card not in hand
    bob_invalid_defense = bob.defend(attack_card, invalid_card)

    # Check if players still have cards after actions
    logger.info(f"Alice has cards: {alice.has_cards()}")
    logger.info(f"Bob has cards: {bob.has_cards()}")

# Run the test
if __name__ == "__main__":
    test_player_module()
