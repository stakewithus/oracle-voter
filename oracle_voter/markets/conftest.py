import pytest
from markets import pricing


@pytest.fixture
def calc_microprice():
    return pricing.calc_microprice
