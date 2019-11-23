import asyncio
import aiohttp
import simplejson as json


async def main():
    target_currency = "LUNA"
    client_session = aiohttp.ClientSession()
    # Get Last Trades
    last_trade_params = { "currency": target_currency, "format": "json" }
    last_trades_resp = await client_session.get(f"https://api.coinone.co.kr/trades/", params=last_trade_params)
    print(last_trades_resp.status)
    raw_text = await last_trades_resp.text()
    last_trades_res = json.loads(raw_text)
    if last_trades_res['errorCode'] != '0':
        # Some error is thrown by the exchange
        raise ValueError(f"Exchange threw error {last_trades_res['errorCode']}")
    # is_ask = the fill is long, the order is ask?
    print(last_trades_res)
    await client_session.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
