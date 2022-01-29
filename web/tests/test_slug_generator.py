from constants import SLUG_LENGTH, SLUG_CHARACTERS, RESERVED_SLUGS
from utils.slug_generator import generate_slug


def test_generator():
    generated = generate_slug()
    assert len(generated) == SLUG_LENGTH
    assert all([c in SLUG_CHARACTERS for c in generated])
    assert generated not in RESERVED_SLUGS
