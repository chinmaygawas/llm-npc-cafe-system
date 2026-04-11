from dialogue import generate_reply

tests = [
    ("Hello! How are you?", 8),
    ("What do you have?", 5),
    ("You're useless.", 2),
    #("Can you tell me about your cafe specials?", 6)
]

for text, rating in tests:
    print(f"\nPlayer ({rating=}): {text}")
    print("NPC:", generate_reply(text, rating))
