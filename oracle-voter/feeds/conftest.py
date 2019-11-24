import pytest
from feeds import coinone


@pytest.fixture
def exchange_coinone_url():
    return "https://api.coinone.co.kr"


@pytest.fixture
def exchange_coinone(exchange_coinone_url):
    return coinone.Coinone(exchange_coinone_url)
