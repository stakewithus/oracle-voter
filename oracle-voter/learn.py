"""
import asyncio
import aiohttp
import simplejson as json


async def main():
    target_currency = "LUNA"
    client_session = aiohttp.ClientSession()
    # Get Last Trades
    orderbook_params = { "currency": target_currency, "format": "json" }

    orderbook_resp = await client_session.get(f"https://api.coinone.co.kr/orderbook/", params=orderbook_params)

    raw_text = await orderbook_resp.text()
    print(raw_text)
    orderbook_res = json.loads(raw_text)
    await client_session.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
"""
