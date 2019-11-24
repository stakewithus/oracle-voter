from aioresponses import aioresponses
import asyncio
from urllib.parse import urlencode
from feeds import fixtures_coinone


def test_get_trades_200(exchange_coinone_url, exchange_coinone):
    target_currency = "LUNA"
    loop = asyncio.get_event_loop()
    with aioresponses() as m:
        mock_param = urlencode({"currency": target_currency, "format": "json"})
        mock_url = f"{exchange_coinone_url}/trades/?{mock_param}"
        m.get(mock_url, status=200, payload=fixtures_coinone.get_trades_200())
        result = loop.run_until_complete(
            exchange_coinone.get_trades(target_currency)
        )
