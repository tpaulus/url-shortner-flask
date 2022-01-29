import random

from constants import SLUG_LENGTH, SLUG_CHARACTERS


def generate_slug() -> str:
    return "".join([random.choice(SLUG_CHARACTERS) for _ in range(SLUG_LENGTH)])
