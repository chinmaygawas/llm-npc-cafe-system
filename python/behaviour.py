from openai import OpenAI

client = OpenAI()

system_prompt = """You are an evaluator in a video game."
                    "Your task is to classify how politely a player speaks to a café receptionist."
                    "Use these rules:"
                    "- polite: friendly, kind, respectful, or complimentary language"
                    "- neutral: short, blunt, or emotionally flat language that is NOT insulting"
                    "- hostile: insulting, aggressive, threatening, or demeaning language"
                    "Examples:"
                    "- 'Hello! You look nice today.' → polite"
                    "- 'What do you want?' → neutral"
                    "- 'You're useless. Get out of my way.' → hostile"
                    "Return ONLY one word: polite, neutral, or hostile."""

def evaluate_behavior(player_text: str) -> str:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": player_text
            }
        ]
    )
    return response.output_text.strip().lower()

if __name__ == "__main__":
    test_inputs = [
        "Hello! How are you?",
        "What do you have?",
        "You are incompetent."
    ]

    for text in test_inputs:
        result = evaluate_behavior(text)
        print(f"Input: {text}")
        print(f"→ Behavior: {result}\n")
