import string
import random


def get_random_string(n: int = 10) -> str:
    """
    Generate random string of len = n
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(n))
