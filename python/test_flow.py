from behaviour import evaluate_behavior
from state import update_rating, get_consequence

rating = 5

player_inputs = [
    "Hello! How are you?",
    "What do you have?",
    "You are incompetent."
]

for text in player_inputs:
    print(f"\nPlayer says: {text}")

    behavior = evaluate_behavior(text)
    print(f"Evaluated behavior: {behavior}")

    rating = update_rating(rating, behavior)
    consequence = get_consequence(rating)

    print(f"Updated rating: {rating}")
    print(f"Consequence: {consequence}")
