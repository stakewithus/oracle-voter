import pytest
from oracle_voter. markets import pricing


@pytest.fixture
def calc_microprice():
    return pricing.calc_microprice
