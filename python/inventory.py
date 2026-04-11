inventory = {
    "coffee": 2,
    "tea": 2,
    "bread": 0
}


def get_inventory():
    return inventory


def available_items():
    return {item: qty for item, qty in inventory.items() if qty > 0}


def unavailable_items():
    return {item: qty for item, qty in inventory.items() if qty == 0}