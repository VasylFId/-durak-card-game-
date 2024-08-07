import logging

def setup_logging():
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
  )

def calculate_score(player):
  # Implement score calculation logic
  score = 0
  for card in player.hand:
    # Simplified score calculation based on the rank
    if card.rank in ['J', 'Q', 'K', 'A']:
      score += 10
    else:
      score += int(card.rank.value)
  return score
