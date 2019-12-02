# Hardcode Supported Markets
from decimal import Decimal, Context
from markets import pricing
from feeds import coinone

WEI_VALUE = Decimal("10.0") ** -18

# Feed Sources
exchange_coinone = coinone.Coinone("https://api.coinone.co.kr")


async def fetch_coinone_krw():
    currency = "LUNA"
    err, orderbook = await exchange_coinone.get_orderbook(currency)
    # Get MicroPrice
    if err is not None:
        raise err
    microprice = pricing.calc_microprice(orderbook)
    return microprice.quantize(WEI_VALUE, context=Context(prec=40))


# Base pair is always uluna for all markets
supported_rates = [{
    "denom": "ukrw",
    "markets": [{
        "pair_type": "native",
        "exchange": "coinone",
        "feed": fetch_coinone_krw,
        "weight": 100,
    }],
}]
