# """
# Unit tests for the RulesManager class in the Durak card game.

# This module contains various tests to ensure that the RulesManager class
# in the game_management module behaves as expected. It includes tests for
# valid attacks, valid defenses, full boards, and card distribution.
# """


# import unittest
# from game_logic.card_package import Card, Suit, Rank
# from game_logic.players import Player
# from game_logic.game_management import BoardManager, RulesManager


# class TestRulesManager(unittest.TestCase):

#     def setUp(self):
#         """
#         Set up a new board manager, trump card, and players before each test.
#         """

#         # Create a new board manager, trump card, and players
#         self.trump_card = Card(Suit.HEARTS, Rank.ACE)  # ♥️A

#         # Set up the board manager
#         self.board_manager = BoardManager(trump_card=self.trump_card)

#         # Set up the players
#         self.attacker = Player(name="Attacker")
#         self.defender = Player(name="Defender")

#     def test_is_valid_attack_empty_board(self):
#         """
#         Test case where the board is empty, so any card can be played as an
#         attack
#         """

#         # Create a card to play as an attack
#         card = Card(Suit.SPADES, Rank.TEN)  # ♠️10

#         # Check if the attack is valid
#         self.assertTrue(RulesManager.is_valid_attack(self.board_manager, card))

#     def test_is_valid_attack_matching_rank(self):
#         """
#         Test case where the board has a card with the same rank, so a card with
#         the same rank can be played as an attack.
#         """

#         # Add a card to the board
#         card1 = Card(Suit.SPADES, Rank.TEN)  # ♠️10
#         card2 = Card(Suit.CLUBS, Rank.TEN)   # ♣️10
#         self.board_manager.add_card_to_board(card1)

#         # Check if the attack of the same rank is valid
#         self.assertTrue(RulesManager.is_valid_attack(self.board_manager,
#                                                      card2))

#     def test_is_valid_attack_non_matching_rank(self):
#         """
#         Test case where the board has a card with a different rank, so a card
#         with a different rank cannot be played as an attack.
#         """

#         # Add cards to the board
#         card1 = Card(Suit.SPADES, Rank.TEN)  # ♠️10
#         card2 = Card(Suit.CLUBS, Rank.NINE)  # ♣️9
#         card3 = Card(Suit.CLUBS, Rank.KING)  # ♣️K
#         self.board_manager.add_card_to_board(card1)
#         self.board_manager.add_card_to_board(card2)

#         # Check if the attack with a different rank is invalid
#         self.assertFalse(RulesManager.is_valid_attack(self.board_manager,
#                                                       card3))

#     def test_is_valid_defense_valid(self):
#         """
#         Test case where the defense is valid based on the game rules.
#         """

#         # Create an attack card and a defense card
#         attack_card = Card(Suit.SPADES, Rank.TEN)
#         defense_card = Card(Suit.SPADES, Rank.JACK)

#         # Check if the defense is valid
#         self.assertTrue(RulesManager.is_valid_defense(self.board_manager,
#                                                       attack_card,
#                                                       defense_card))

#     def test_is_valid_defense_invalid(self):
#         """
#         Test case where the defense is invalid based on the game rules.
#         """

#         # Create an attack card and a defense card
#         attack_card = Card(Suit.SPADES, Rank.TEN)    # ♠️10
#         defense_card = Card(Suit.SPADES, Rank.NINE)  # ♠️9

#         # Check if the defense is invalid
#         self.assertFalse(RulesManager.is_valid_defense(self.board_manager,
#                                                        attack_card,
#                                                        defense_card))

#     def test_is_valid_defense_trump_ace_invalid(self):
#         """
#         Test case where the defense is invalid because the attack card is a
#         trump card (Ace).
#         """

#         # Create an attack card and a defense card
#         attack_card = Card(Suit.HEARTS, Rank.ACE)   # ♥️A (trump card)
#         defense_card = Card(Suit.SPADES, Rank.TEN)  # ♠️10

#         # Check if the defense is invalid
#         self.assertFalse(RulesManager.is_valid_defense(self.board_manager,
#                                                        attack_card,
#                                                        defense_card))

#     def test_is_valid_defense_trump_card(self):
#         """
#         Test case where the defense is valid because the defense card is a
#         trump card.
#         """

#         # Create an attack card and a defense card
#         attack_card = Card(Suit.SPADES, Rank.TEN)   # ♠️10
#         defense_card = Card(Suit.HEARTS, Rank.SIX)  # ♥️6 (trump card)
#         self.assertTrue(RulesManager.is_valid_defense(self.board_manager,
#                                                       attack_card,
#                                                       defense_card))

#     def test_is_board_full_first_round(self):
#         """
#         Test case where the board is not full in the first round.
#         """

#         # Simulate adding 10 cards to the board
#         for _ in range(10):
#             self.board_manager.add_card_to_board(Card(Suit.SPADES, Rank.TEN))

#         # Check if the board is full
#         self.assertTrue(RulesManager.is_board_full(self.board_manager))

#     def test_is_board_full_subsequent_rounds(self):
#         """
#         Test case where the board is full in subsequent rounds.
#         """

#         # Simulate moving to the second round
#         self.board_manager.next_round()  # Move to round 2

#         # Simulate adding 12 cards to the board
#         for _ in range(12):
#             self.board_manager.add_card_to_board(Card(Suit.SPADES, Rank.TEN))

#         # Check if the board is full
#         self.assertTrue(RulesManager.is_board_full(self.board_manager))

#     def test_full_hands_no_pickup(self):
#         """
#         Test case where both players have full hands (6 cards each), so no
#         cards should be picked up.
#         """

#         # Set up the players with full hands
#         self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),    # ♠️10
#                               Card(Suit.SPADES, Rank.NINE),   # ♠️9
#                               Card(Suit.SPADES, Rank.EIGHT),  # ♠️8
#                               Card(Suit.SPADES, Rank.SEVEN),  # ♠️7
#                               Card(Suit.SPADES, Rank.SIX),    # ♠️6
#                               Card(Suit.SPADES, Rank.KING)]   # ♠️K
#         self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),     # ♣️10
#                               Card(Suit.CLUBS, Rank.NINE),    # ♣️9
#                               Card(Suit.CLUBS, Rank.EIGHT),   # ♣️8
#                               Card(Suit.CLUBS, Rank.SEVEN),   # ♣️7
#                               Card(Suit.CLUBS, Rank.SIX),     # ♣️6
#                               Card(Suit.CLUBS, Rank.KING)]    # ♣️K
#         deck_size = 10

#         result = RulesManager.determine_card_distribution(deck_size,
#                                                           self.attacker,
#                                                           self.defender)

#         # Both players have full hands, so no cards should be picked up
#         self.assertEqual(result, {"attacker": 0, "defender": 0})

#     def test_attacker_needs_cards(self):
#         """
#         Test case where only the attacker needs cards, and the deck has enough
#         cards.
#         """

#         # Set up the players with hands that need cards
#         self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),    # ♠️10
#                               Card(Suit.SPADES, Rank.NINE),   # ♠️9
#                               Card(Suit.SPADES, Rank.EIGHT),  # ♠️8
#                               Card(Suit.SPADES, Rank.SEVEN)]  # ♠️7
#         self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),     # ♣️10
#                               Card(Suit.CLUBS, Rank.NINE),    # ♣️9
#                               Card(Suit.CLUBS, Rank.EIGHT),   # ♣️8
#                               Card(Suit.CLUBS, Rank.SEVEN),   # ♣️7
#                               Card(Suit.CLUBS, Rank.SIX),     # ♣️6
#                               Card(Suit.CLUBS, Rank.KING)]    # ♣️K
#         deck_size = 10

#         result = RulesManager.determine_card_distribution(deck_size,
#                                                           self.attacker,
#                                                           self.defender)

#         # Attacker needs 2 cards, defender needs 0 cards
#         self.assertEqual(result, {"attacker": 2, "defender": 0})

#     def test_defender_needs_cards(self):
#         """
#         Test case where only the defender needs cards, and the deck has enough
#         cards.
#         """

#         # Set up the players with hands that need cards
#         self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),    # ♠️10
#                               Card(Suit.SPADES, Rank.NINE),   # ♠️9
#                               Card(Suit.SPADES, Rank.EIGHT),  # ♠️8
#                               Card(Suit.SPADES, Rank.SEVEN),  # ♠️7
#                               Card(Suit.SPADES, Rank.SIX),    # ♠️6
#                               Card(Suit.SPADES, Rank.KING)]   # ♠️K
#         self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),     # ♣️10
#                               Card(Suit.CLUBS, Rank.NINE)]    # ♣️9

#         deck_size = 10

#         result = RulesManager.determine_card_distribution(deck_size,
#                                                           self.attacker,
#                                                           self.defender)

#         # Attacker needs 0 cards, defender needs 4 cards
#         self.assertEqual(result, {"attacker": 0, "defender": 4})

#     def test_both_need_cards_enough_in_deck(self):
#         """
#         Test case where both players need cards, and the deck has enough cards
#         for both.
#         """

#         self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),    # ♠️10
#                               Card(Suit.SPADES, Rank.NINE),   # ♠️9
#                               Card(Suit.SPADES, Rank.EIGHT)]  # ♠️8
#         self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),     # ♣️10
#                               Card(Suit.CLUBS, Rank.NINE),    # ♣️9
#                               Card(Suit.CLUBS, Rank.EIGHT)]   # ♣️8

#         deck_size = 6  # Enough to give 3 to attacker and 3 to defender

#         result = RulesManager.determine_card_distribution(deck_size,
#                                                           self.attacker,
#                                                           self.defender)

#         # Attacker needs 3 cards, defender needs 3 cards
#         self.assertEqual(result, {"attacker": 3, "defender": 3})

#     def test_both_need_cards_not_enough_in_deck(self):
#         """
#         Test case where both players need cards, but the deck does not have
#         enough cards.
#         """

#         # Set up the players with hands that need cards
#         self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),    # ♠️10
#                               Card(Suit.SPADES, Rank.NINE),   # ♠️9
#                               Card(Suit.SPADES, Rank.EIGHT),  # ♠️8
#                               Card(Suit.SPADES, Rank.SEVEN)]  # ♠️7
#         self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),     # ♣️10
#                               Card(Suit.CLUBS, Rank.NINE)]    # ♣️9
#         deck_size = 4  # Not enough cards to satisfy both players

#         result = RulesManager.determine_card_distribution(deck_size,
#                                                           self.attacker,
#                                                           self.defender)

#         # Attacker needs 2 cards, defender needs 2 cards
#         self.assertEqual(result, {"attacker": 2, "defender": 2})

#     def test_both_need_cards_exact_amount_in_deck(self):
#         """
#         Test case where both players need cards, and the deck has the exact
#         amount needed.
#         """

#         # Set up the players with hands that need cards
#         self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),    # ♠️10
#                               Card(Suit.SPADES, Rank.NINE)]   # ♠️9
#         self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),     # ♣️10
#                               Card(Suit.CLUBS, Rank.NINE),    # ♣️9
#                               Card(Suit.CLUBS, Rank.EIGHT),   # ♣️8
#                               Card(Suit.CLUBS, Rank.SEVEN)]   # ♣️7

#         deck_size = 6  # Just enough cards to split

#         result = RulesManager.determine_card_distribution(deck_size,
#                                                           self.attacker,
#                                                           self.defender)

#         # Attacker needs 2 cards, defender needs 2 cards
#         self.assertEqual(result, {"attacker": 4, "defender": 2})

#     def test_attacker_needs_cards_but_deck_empty(self):
#         """
#         Test case where the attacker needs cards, but the deck is empty.
#         """

#         # Set up the players with hands that need cards
#         self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),    # ♠️10
#                               Card(Suit.SPADES, Rank.NINE),   # ♠️9
#                               Card(Suit.SPADES, Rank.EIGHT),  # ♠️8
#                               Card(Suit.SPADES, Rank.SEVEN)]  # ♠️7
#         self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),     # ♣️10
#                               Card(Suit.CLUBS, Rank.NINE),    # ♣️9
#                               Card(Suit.CLUBS, Rank.EIGHT),   # ♣️8
#                               Card(Suit.CLUBS, Rank.SEVEN),   # ♣️7
#                               Card(Suit.CLUBS, Rank.SIX),     # ♣️6
#                               Card(Suit.CLUBS, Rank.KING)]    # ♣️K

#         deck_size = 0  # Empty deck

#         result = RulesManager.determine_card_distribution(deck_size,
#                                                           self.attacker,
#                                                           self.defender)

#         # Attacker needs 2 cards, but the deck is empty
#         self.assertEqual(result, {"attacker": 0, "defender": 0})

#     def test_both_players_need_cards_deck_nearly_empty(self):
#         """
#         Test case where both players need cards, but the deck has very few
#         cards left.
#         """

#         # Set up the players with hands that need cards
#         self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),    # ♠️10
#                               Card(Suit.SPADES, Rank.NINE)]   # ♠️9
#         self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),     # ♣️10
#                               Card(Suit.CLUBS, Rank.NINE)]    # ♣️9

#         deck_size = 2  # Only 1 card left for each player

#         result = RulesManager.determine_card_distribution(deck_size,
#                                                           self.attacker,
#                                                           self.defender)

#         # In this case, one player will get the only card left
#         self.assertEqual(result, {"attacker": 1, "defender": 1})

#     def test_both_players_have_more_than_six_cards(self):
#         """
#         Test case where both players have more than 6 cards and don't need to
#         pick up any cards.
#         """

#         # Set up the players with hands that have more than 6 cards
#         self.attacker.hand = [Card(Suit.SPADES, Rank.TEN),    # ♠️10
#                               Card(Suit.SPADES, Rank.NINE),   # ♠️9
#                               Card(Suit.SPADES, Rank.EIGHT),  # ♠️8
#                               Card(Suit.SPADES, Rank.SEVEN),  # ♠️7
#                               Card(Suit.SPADES, Rank.SIX),    # ♠️6
#                               Card(Suit.SPADES, Rank.KING),   # ♠️K
#                               Card(Suit.SPADES, Rank.QUEEN)]  # ♠️Q
#         self.defender.hand = [Card(Suit.CLUBS, Rank.TEN),     # ♣️10
#                               Card(Suit.CLUBS, Rank.NINE),    # ♣️9
#                               Card(Suit.CLUBS, Rank.EIGHT),   # ♣️8
#                               Card(Suit.CLUBS, Rank.SEVEN),   # ♣️7
#                               Card(Suit.CLUBS, Rank.SIX),     # ♣️6
#                               Card(Suit.CLUBS, Rank.KING),    # ♣️K
#                               Card(Suit.CLUBS, Rank.QUEEN)]   # ♣️Q

#         deck_size = 10

#         result = RulesManager.determine_card_distribution(deck_size,
#                                                           self.attacker,
#                                                           self.defender)

#         # Both players have more than 6 cards, so no cards should be picked up
#         self.assertEqual(result, {"attacker": 0, "defender": 0})


# if __name__ == '__main__':
#     unittest.main()
