MIN_RATING = 1
MAX_RATING = 10
LOCKOUT_THRESHOLD = 1


def update_rating(current_rating: int, behavior: str) -> int:
    if behavior == "polite":
        current_rating += 1
    elif behavior == "hostile":
        current_rating -= 1
    # neutral -> no change

    current_rating = max(MIN_RATING, min(MAX_RATING, current_rating))
    return current_rating


def get_consequence(rating: int) -> str:
    if rating <= LOCKOUT_THRESHOLD:
        return "locked_out"
    elif rating <= 4:
        return "price_hike"
    elif rating >= 7:
        return "discount"
    else:
        return "normal"
