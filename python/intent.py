from openai import OpenAI

client = OpenAI()


def detect_intent(player_text: str, pending_order):
    order_context = f"Pending order: {pending_order}"

    system_prompt = """
                    You are an intent classifier for a café ordering system.

                    Classify the player's message into one of these intents:

                    order   → player wants to buy an item
                    confirm → player confirms a purchase
                    cancel  → player cancels a purchase
                    none    → any other conversation

                    If the intent is "order", also identify the item mentioned.

                    Possible items:
                    coffee
                    tea
                    bread

                    Examples:

                    Player: "I would like tea"
                    Response: {"intent": "order", "item": "tea"}

                    Player: "yes"
                    Response: {"intent": "confirm"}

                    Player: "cancel that"
                    Response: {"intent": "cancel"}

                    Player: "hello"
                    Response: {"intent": "none"}
                    
                    {order_context}

                    If a pending order exists and the player says things like
                    "yes", "sure", "ok", "alright", "absolutely" or any word/phrase that can be a positive answer to a question like "would you like to confirm your order?", treat it as CONFIRM.

                    Respond ONLY in JSON.
                    """

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": player_text}
        ]
    )

    return response.output[0].content[0].text