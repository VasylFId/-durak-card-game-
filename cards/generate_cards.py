import os
from PIL import Image, ImageDraw, ImageFont

# Define card suits (using emojis) and ranks
suits = {
    'hearts': '♥️',
    'diamonds': '♦️',
    'clubs': '♣️',
    'spades': '♠️'
}
ranks = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Create a directory for the card images
if not os.path.exists('card_images'):
    os.makedirs('card_images')

# Function to create a card image
def create_card_image(rank, suit):
    # Create a blank white image
    card = Image.new('RGB', (200, 300), color='white')
    draw = ImageDraw.Draw(card)

    # Add a border
    draw.rectangle([10, 10, 190, 290], outline='black', width=2)

    # Add rank
    font_rank = ImageFont.truetype("arial.ttf", 36)
    draw.text((20, 20), rank, fill='black', font=font_rank)
    draw.text((160, 250), rank, fill='black', font=font_rank)

    # Add suit (emoji)
    font_suit = ImageFont.truetype("seguiemj.ttf", 72)  # Use a font that supports emojis
    draw.text((85, 110), suits[suit], fill='black' if suit in ['clubs', 'spades'] else 'red', font=font_suit)

    # Save the card image
    card.save(f'card_images/{rank}_of_{suit}.png')

# Generate all cards
for suit in suits:
    for rank in ranks:
        create_card_image(rank, suit)

print("All card images have been generated and saved in the 'card_images' directory.")