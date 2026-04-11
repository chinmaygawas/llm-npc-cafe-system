import json
import random
from fastapi import FastAPI
from pydantic import BaseModel

from behaviour import evaluate_behavior
from state import update_rating, get_consequence
from dialogue import generate_reply
from inventory import get_inventory
from intent import detect_intent
from prices import get_prices

app = FastAPI()

# Starting rating
rating = 5
pending_order = None
purchase_made = None
purchase_history = []
locked_price = None


class PlayerMessage(BaseModel):
    player_text: str


@app.post("/chat")
def chat(message: PlayerMessage):
    global rating, pending_order, purchase_made, purchase_history, locked_price

    purchase_price = None

    player_text = message.player_text

    #Evaluate behavior
    behavior = evaluate_behavior(player_text)

    #Update rating
    rating = update_rating(rating, behavior)

    # Get inventory
    inventory = get_inventory()
    prices = get_prices()
    adjusted_prices = prices.copy()

    menu_items = list(inventory.keys())
    text = player_text.lower()
    mentioned_items = [item for item in menu_items if item in text.split()]

    #Determine consequence
    consequence = get_consequence(rating)
    if pending_order is None:
        if consequence == "discount":
            adjusted_prices = {item: int(price * 0.9) for item, price in prices.items()}

        elif consequence == "penalty":
            adjusted_prices = {item: int(price * 1.2) for item, price in prices.items()}

    # MULTIPLE ITEM REQUEST
    if len(mentioned_items) > 1:
        options = " or ".join(mentioned_items)

        reply = f"I can serve one item at a time. Would you like {options}?"

        return {
            "reply": reply,
            "rating": rating,
            "consequence": consequence,
            "inventory": inventory,
            "intent_result": "multiple_items"
        }

    #Detect intent
    intent_result = detect_intent(player_text, pending_order)
    print("Intent raw output:", intent_result)
    intent_clean = intent_result.replace("```json", "").replace("```", "").strip()
    try:
        intent_data = json.loads(intent_clean)
    except:
        intent_data = {"intent": "none"}
    print(intent_clean)

    intent = intent_data.get("intent")
    item = intent_data.get("item")

    # VALIDATE ITEM EXISTS IN INVENTORY
    if intent == "order" and item:
        if item not in inventory:
            reply = f"I'm afraid we don't serve {item} here."

            return {
                "reply": reply,
                "rating": rating,
                "consequence": consequence,
                "inventory": inventory,
                "intent_result": intent_clean
            }

    # ORDER REQUEST
    if intent == "order" and item:
        if inventory.get(item, 0) > 0:
            pending_order = item
            locked_price = adjusted_prices[item]

    # CONFIRM PURCHASE
    elif intent == "confirm" and pending_order:
        inventory[pending_order] -= 1
        purchase_made = pending_order
        purchase_history.append(pending_order)
        purchase_price = locked_price
        pending_order = None
        locked_price = None

    # CANCEL ORDER
    elif intent == "cancel":
        pending_order = None
        locked_price = None

    # DEBUG LINE
    print("DEBUG → pending_order: ", pending_order)
    print("DEBUG → purchase_made: ", purchase_made)
    print("Inventory: ", inventory)
    print("Rating: ", rating)
    print("Cost: ", adjusted_prices)
    print("Purchase History: ", purchase_history)

    #Generate NPC reply

    if purchase_made:
        purchase_lines = [
            f"Great! Here's your {purchase_made}. Enjoy!",
            f"Your {purchase_made} is ready. Hope you like it!",
            f"One {purchase_made} coming right up. Enjoy!"
        ]

        reply = random.choice(purchase_lines)
    else:
        reply = generate_reply(player_text, rating, inventory, pending_order, purchase_made, purchase_history, adjusted_prices)

    purchase_made = None

    return {
        "reply": reply,
        "rating": rating,
        "consequence": consequence,
        "inventory": inventory,
        "intent_result": intent_clean,
        "purchase_history": purchase_history,
        "prices": adjusted_prices,
        "locked_price": locked_price,
        "purchase_price": purchase_price
    }