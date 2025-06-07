import random
from datetime import datetime


def random_number_tool() -> int:
    """
    Generate a random integer between 1 and 100.
    """
    return random.randint(1, 100)


def date_tool() -> str:
    """
    Return today's date in YYYY-MM-DD format.
    """
    return datetime.utcnow().date().isoformat()
