import asyncio
import pytest
from unittest.mock import Mock, patch
from oracle_voter.common.util import (
    async_stubber,
    async_raiser,
    not_found
)
from oracle_voter.feeds.markets import fetch_coinone_krw, derive_rate
from oracle_voter.feeds.fixtures_coinone import get_orderbook_200
from oracle_voter.feeds.markets import ExchangeErr


@patch('oracle_voter.common.client.http_get')
def test_fetch_coinone_krw(http_mock, exchange_coinone):
    http_mock.return_value = async_stubber(get_orderbook_200())
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        fetch_coinone_krw()
    )
    assert str(result) == "263.563000000000000000"
    

@patch('oracle_voter.common.client.http_get')
def test_fetch_coinone_krw_error(http_mock, exchange_coinone):
    http_mock.return_value = async_stubber({"errorCode":"51"})
    loop = asyncio.get_event_loop()
    with pytest.raises(ExchangeErr):
        loop.run_until_complete(
            fetch_coinone_krw()
        )
        

@patch('oracle_voter.common.client.http_get')
def test_derive_rate(http_mock):
    http_mock.return_value = async_stubber([[1578626600000, 2.3255122144959466], [1578626659000, 2.32551221449594322]])
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        derive_rate("mnt")
    )
    http_mock.assert_called_with(
        "https://api.ukfx.co.uk/pairs/krw/mnt/livehistory/chart?t=1")
    assert str(result) == "2.325512214495943031"
        

@patch('oracle_voter.common.client.http_get')
def test_derive_rate_error(http_mock):
    http_mock.return_value = async_stubber(None)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        derive_rate("mnt")
    )
    assert str(result) == "-1.000000000000000000"
