import logging
import random

from constants import SLUG_LENGTH, SLUG_CHARACTERS, RESERVED_SLUGS

log = logging.getLogger(__name__)


def generate_slug() -> str:
    while True:
        slug = "".join([random.choice(SLUG_CHARACTERS) for _ in range(SLUG_LENGTH)])
        if slug not in RESERVED_SLUGS:
            return slug
        else:
            log.warning("You should buy a lottery ticket. The random slug generator generated a reserved slug.")
