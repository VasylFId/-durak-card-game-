# """
# Unit tests for the TurnManager class in the Durak game.

# This module contains various tests to ensure that the TurnManager class is
# working as expected. It includes tests to check if the attack is valid, if the
# defense is valid, if the turn can be switched, and if the second attack or
# defense is successful or unsuccessful.
# """


# import unittest
# from game_logic.card_package import Card, Suit, Rank
# from game_logic.players import Player
# from game_logic.game_management import BoardManager, TurnManager, PlayerManager


# class TestTurnManager(unittest.TestCase):

#     def setUp(self):
#         """
#         Set up the TurnManager with two players, each with a hand of 6 cards.
#         """

#         # Set up two players
#         self.attacker = Player(name="Alice")
#         self.defender = Player(name="Bob")

#         # Set up a trump suit for both players
#         self.trump_card = Card(Suit.HEARTS, Rank.KING)  # ♥️K
#         PlayerManager.set_player_trump_suit(self.attacker, self.trump_card)
#         PlayerManager.set_player_trump_suit(self.defender, self.trump_card)

#         # Set up a board manager
#         self.board_manager = BoardManager(trump_card=self.trump_card)

#         # Give each player 6 cards
#         attacker_cards = [
#             Card(Suit.CLUBS, Rank.SIX),         # ♣️6
#             Card(Suit.CLUBS, Rank.TEN),         # ♣️10
#             Card(Suit.DIAMONDS, Rank.SEVEN),    # ♦️7
#             Card(Suit.SPADES, Rank.KING),       # ♠️K
#             Card(Suit.HEARTS, Rank.EIGHT),      # ♥️8
#             Card(Suit.HEARTS, Rank.JACK)        # ♥️J
#         ]

#         defender_cards = [
#             Card(Suit.DIAMONDS, Rank.SIX),      # ♦️6
#             Card(Suit.DIAMONDS, Rank.QUEEN),    # ♦️Q
#             Card(Suit.CLUBS, Rank.EIGHT),       # ♣️8
#             Card(Suit.CLUBS, Rank.KING),        # ♣️K
#             Card(Suit.HEARTS, Rank.SEVEN),      # ♥️7
#             Card(Suit.HEARTS, Rank.TEN)         # ♥️10
#         ]

#         for card in attacker_cards:
#             PlayerManager.add_card_to_hand(self.attacker, card)
#             # [♥️J, ♥️8, ♠️K, ♣️10, ♠️7, ♣️6]

#         for card in defender_cards:
#             PlayerManager.add_card_to_hand(self.defender, card)
#             # [♥️10, ♥️7, ♣️K, ♣️8, ♦️Q, ♦️6]

#         # Set up the TurnManager
#         self.turn_manager = TurnManager(attacker=self.attacker,
#                                         defender=self.defender,
#                                         board_manager=self.board_manager)

#     def test_execute_attack(self):
#         """
#         Test the execute_attack method of the TurnManager.
#         """

#         # Attacker plays a card

#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♣️6
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[-1]

#         # Execute the attack
#         self.turn_manager.execute_attack(card_to_attack)

#         # Check if the attack was successful
#         self.assertEqual(self.turn_manager.turn_state["attacks"],
#                          [card_to_attack])

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, False)
#         self.assertEqual(self.turn_manager.is_defender_turn, True)

#     def test_handle_defense(self):
#         """
#         Test the handle_defense method of the TurnManager.
#         """

#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♣️6
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[-1]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Defender plays a card
#         # Defender plays the last card in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♦️6
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[-1]

#         # Defender can't beat the attacking card, but he has options to
#         # continue defense with other card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)
#         self.assertEqual(self.turn_manager.turn_state["defenses"], [])

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, False)
#         self.assertEqual(self.turn_manager.is_defender_turn, True)

#     def test_successful_defense(self):
#         """
#         Test the handle_defense method of the TurnManager.
#         """
#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♣️6
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[-1]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Defender plays a card
#         # Defender plays the last card in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♣️8
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[-2]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)
#         self.assertEqual(self.turn_manager.turn_state["defenses"],
#                          [card_to_defend])

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, True)
#         self.assertEqual(self.turn_manager.is_defender_turn, False)

#     def test_switch_turn(self):
#         """
#         Test the switch_turn method of the TurnManager.
#         """
#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♣️6
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[-1]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Defender plays a card
#         # Defender plays the last card in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♣️8
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[-2]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Switch turn
#         self.turn_manager.switch_turn()

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, True)
#         self.assertEqual(self.turn_manager.is_defender_turn, False)

#     def test_succesful_second_attack(self):
#         """
#         Test the execute_attack method of the TurnManager.
#         """
#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♣️6
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[-1]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Defender plays a card
#         # Defender plays the last card in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♣️8
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[-2]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♥️8
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[1]
#         self.turn_manager.execute_attack(card_to_attack)

#         self.assertEqual(self.turn_manager.turn_state["attacks"][-1],
#                          card_to_attack)

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, False)
#         self.assertEqual(self.turn_manager.is_defender_turn, True)

#     def test_unsuccessful_second_attack(self):
#         """
#         Test the execute_attack method of the TurnManager.
#         """
#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♣️6
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[-1]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Defender plays a card
#         # Defender plays the last card in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♣️8
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[-2]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♥️J
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[0]
#         self.turn_manager.execute_attack(card_to_attack)

#         self.assertNotEqual(self.turn_manager.turn_state["attacks"][-1],
#                             card_to_attack)

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, True)
#         self.assertEqual(self.turn_manager.is_defender_turn, False)

#     def test_succesful_second_defense(self):
#         """
#         Test the handle_defense method of the TurnManager.
#         """
#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♣️6
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[-1]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Defender plays a card
#         # Defender plays the last card in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♣️8
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[-2]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♥️8
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[1]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Defender plays a card
#         # Defender plays the first card in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♥️10
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[0]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Check if the defense was successful
#         self.assertEqual(self.turn_manager.turn_state["defenses"][-1],
#                          card_to_defend)

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, True)
#         self.assertEqual(self.turn_manager.is_defender_turn, False)

#     def test_unsuccessful_second_defense(self):
#         """
#         Test the handle_defense method of the TurnManager.
#         """

#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♣️6
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[-1]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Defender plays a card
#         # Defender plays the last card in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♣️8
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[-2]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♥️J
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[0]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Attacker plays a card again
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♥️8
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[1]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Defender plays a card
#         # Defender plays the third card in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♣️K
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[2]

#         # Defender can't beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Check if the defense was unsuccessful
#         self.assertEqual(
#             card_to_defend in self.turn_manager.turn_state["defenses"], False)

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, False)
#         self.assertEqual(self.turn_manager.is_defender_turn, True)

#         # Defender plays a card
#         # Defender plays the first card in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♥️10
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[0]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Check if the defense was successful
#         self.assertEqual(self.turn_manager.turn_state["defenses"][-1],
#                          card_to_defend)

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, True)
#         self.assertEqual(self.turn_manager.is_defender_turn, False)

#     def test_mixed_turns(self):
#         """
#         Test the switch_turn method of the TurnManager.
#         """

#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♣️6
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[-1]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Defender plays a card
#         # Defender plays the last card in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♣️8
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[-2]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♥️8
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[1]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Switch turn
#         self.turn_manager.switch_turn()

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, False)
#         self.assertEqual(self.turn_manager.is_defender_turn, True)

#         # Defender plays a card
#         # Defender plays the last card in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♥️10
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[0]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Switch turn
#         self.turn_manager.switch_turn()

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, True)
#         self.assertEqual(self.turn_manager.is_defender_turn, False)

#         # Attacker plays a card
#         # Attacker plays the prelast card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♣️10
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[-2]
#         self.turn_manager.execute_attack(card_to_attack)

#         # Switch turn
#         self.turn_manager.switch_turn()

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, False)
#         self.assertEqual(self.turn_manager.is_defender_turn, True)

#         # Defender plays a card
#         # Defender plays the 3rd card from right in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♣️K
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[-3]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Switch turn
#         self.turn_manager.switch_turn()

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, True)
#         self.assertEqual(self.turn_manager.is_defender_turn, False)

#         # Attacker plays a card
#         # Attacker plays the second card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♠️K
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[1]

#         # Attacker can't attack with the same card
#         self.turn_manager.execute_attack(card_to_attack)

#         # Switch turn
#         self.turn_manager.switch_turn()

#         self.assertEqual(self.turn_manager.is_attacker_turn, False)
#         self.assertEqual(self.turn_manager.is_defender_turn, True)

#         # Defender plays a card
#         # Defender plays the 1st card from left in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♥️7
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[0]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Switch turn
#         self.turn_manager.switch_turn()

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, True)
#         self.assertEqual(self.turn_manager.is_defender_turn, False)

#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♦️7
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[-1]

#         # Attacker can't attack with the same card
#         self.turn_manager.execute_attack(card_to_attack)

#         # Switch turn
#         self.turn_manager.switch_turn()

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, False)
#         self.assertEqual(self.turn_manager.is_defender_turn, True)

#         # Defender plays a card
#         # Defender plays the 1st card from left in their hand to defend
#         # Taken from PlayerManager
#         # Expected card: ♦️Q
#         card_to_defend = PlayerManager.get_player_hand(self.defender)[0]

#         # Defender can beat the attacking card
#         self.turn_manager.handle_defense(card_to_attack, card_to_defend)

#         # Switch turn
#         self.turn_manager.switch_turn()

#         # Check if the turn was switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, True)
#         self.assertEqual(self.turn_manager.is_defender_turn, False)

#         # Attacker plays a card
#         # Attacker plays the last card in their hand to attack
#         # Taken from PlayerManager
#         # Expected card: ♥️J
#         card_to_attack = PlayerManager.get_player_hand(self.attacker)[-1]

#         # Attack is invalid since it is the 1st round and
#         # the attacker can't attack more than 5 cards
#         self.turn_manager.execute_attack(card_to_attack)

#         # Switch turn
#         self.turn_manager.switch_turn()

#         # Check if the turn was not switched
#         self.assertEqual(self.turn_manager.is_attacker_turn, True)
#         self.assertEqual(self.turn_manager.is_defender_turn, False)


# if __name__ == '__main__':
#     unittest.main()
