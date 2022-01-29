import pytest


@pytest.fixture
def endpoint() -> str:
    # Change this if you want to run the tests against a different endpoint

    return "http://127.0.0.1"
