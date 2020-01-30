import asyncio

from oracle_voter.feeds.coinone import Coinone


def test_get_orderbook_success():
    feed = Coinone()
    loop = asyncio.get_event_loop()

    result = loop.run_until_complete(
        feed.get_orderbook("LUNA")
    )
    print(result)
