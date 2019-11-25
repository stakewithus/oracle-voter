from aioresponses import aioresponses
import asyncio
from urllib.parse import urlencode
from feeds import fixtures_coinone
from decimal import Decimal


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
        print(trades[0:5])
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
