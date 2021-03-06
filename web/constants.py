from typing import Final, Set, List

MAX_SLUG_GENERATION_ATTEMPTS: Final[int] = 3
RESERVED_SLUGS: Final[Set[str]] = {"stats", "slugs"}

SLUG_LENGTH: Final[int] = 8
SLUG_CHARACTERS: Final[List[str]] = list("cdefhjkmnprtvwxy2345689")  # Non-ambiguous lowercase characters
