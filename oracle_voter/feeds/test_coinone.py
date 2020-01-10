from aioresponses import aioresponses
import asyncio
from urllib.parse import urlencode
from oracle_voter.feeds import fixtures_coinone
from decimal import Decimal
from unittest.mock import Mock, patch
from oracle_voter.common.util import (
    async_stubber,
    async_raiser,
    not_found
)


def test_get_trades_200(exchange_coinone_url, exchange_coinone):
    target_currency = "LUNA"
    loop = asyncio.get_event_loop()
    with aioresponses() as m:
        mock_param = urlencode({"currency": target_currency, "format": "json"})
        mock_url = f"{exchange_coinone_url}/trades/?{mock_param}"
        m.get(mock_url, status=200, payload=fixtures_coinone.get_trades_200())
        error, result = loop.run_until_complete(
            exchange_coinone.get_trades(target_currency)
        )
        assert error is None
        trades = result["trades"]
        ts_1, px_1, qty_1, side_1 = trades[0]
        assert ts_1 == "1574592036"
        assert px_1 == Decimal("297.0")
        assert qty_1 == Decimal("21.7188")
        assert side_1 == 0
        ts_last, px_last, qty_last, side_last = trades[len(trades) - 1]
        assert ts_last == "1574586897"
        assert px_last == Decimal("297.0")
        assert qty_last == Decimal("773.1255")
        assert side_last == 0


def test_get_trades_200_exchange_error_code(
    exchange_coinone_url,
    exchange_coinone,
):
    target_currency = "LUNA"
    loop = asyncio.get_event_loop()
    with aioresponses() as m:
        mock_param = urlencode({"currency": target_currency, "format": "json"})
        mock_url = f"{exchange_coinone_url}/trades/?{mock_param}"
        m.get(
            mock_url,
            status=200,
            payload=fixtures_coinone.get_trades_200_exchange_error_code(),
        )
        error, result = loop.run_until_complete(
            exchange_coinone.get_trades(target_currency)
        )
        assert error is not None


def test_get_orderbook_200(exchange_coinone_url, exchange_coinone):
    target_currency = "LUNA"
    loop = asyncio.get_event_loop()
    with aioresponses() as m:
        mock_param = urlencode({"currency": target_currency, "format": "json"})
        mock_url = f"{exchange_coinone_url}/orderbook/?{mock_param}"
        m.get(
            mock_url,
            status=200,
            payload=fixtures_coinone.get_orderbook_200(),
        )
        error, result = loop.run_until_complete(
            exchange_coinone.get_orderbook(target_currency)
        )
        assert error is None
        top_asks = [
            (Decimal('264.0'), Decimal('3583.053')),
            (Decimal('265.0'), Decimal('378.8709')),
            (Decimal('266.0'), Decimal('601.7191')),
        ]
        assert result["asks"][0:3] == top_asks
        top_bids = [
            (Decimal('263.0'), Decimal('609.1189')),
            (Decimal('262.0'), Decimal('749.1645')),
            (Decimal('261.0'), Decimal('2179.129')),
        ]
        assert result["bids"][0:3] == top_bids


@patch('oracle_voter.common.client.http_get')
def test_get_orderbook_exception(http_mock, exchange_coinone):
    http_mock.return_value = not_found()
    loop = asyncio.get_event_loop()
    error, result = loop.run_until_complete(
        exchange_coinone.get_orderbook("LUNA")
    )
    assert error is not None
    assert result is None
    

@patch('oracle_voter.common.client.http_get')
def test_get_orderbook_error(http_mock, exchange_coinone):
    http_mock.return_value = async_stubber({"errorCode": 400})
    loop = asyncio.get_event_loop()
    error, _ = loop.run_until_complete(
        exchange_coinone.get_orderbook("LUNA")
    )
    assert error is 400
