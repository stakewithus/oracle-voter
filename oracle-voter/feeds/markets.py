# Hardcode Supported Markets
from decimal import Decimal, Context
from markets import pricing
from feeds import coinone, ukfx
from functools import partial

WEI_VALUE = Decimal("10.0") ** -18

# Feed Sources
exchange_coinone = coinone.Coinone("https://api.coinone.co.kr")

feed_ukfx = ukfx.UKFX("https://api.ukfx.co.uk")


async def fetch_coinone_krw():
    currency = "LUNA"
    err, orderbook = await exchange_coinone.get_orderbook(currency)
    # Get MicroPrice
    if err is not None:
        raise err
    microprice = pricing.calc_microprice(orderbook)
    return microprice.quantize(WEI_VALUE, context=Context(prec=40))


async def derive_rate(target):
    base_currency = "krw"
    raw_px = await feed_ukfx.get_swap(base_currency, target)
    return Decimal(raw_px).quantize(WEI_VALUE, context=Context(prec=40))


# Base pair is always uluna for all markets
supported_rates = [{
    "denom": "ukrw",
    "pair_type": "native",
    "markets": [{
        "exchange": "coinone",
        "feed": fetch_coinone_krw,
        "weight": 100,
    }],
  }, {
    "denom": "umnt",
    "pair_type": "derivative",
    "markets": [{
        "feed": partial(derive_rate, "mnt"),
        "weight": 100,
    }],
  }, {
    "denom": "uusd",
    "pair_type": "derivative",
    "markets": [{
        "feed": partial(derive_rate, "usd"),
        "weight": 100,
    }],
  }, {
    "denom": "usdr",
    "pair_type": "derivative",
    "markets": [{
        "feed": partial(derive_rate, "xdr"),
        "weight": 100,
    }],
}]
