# Hardcode Supported Markets
from decimal import Decimal, Context
from functools import partial

from oracle_voter.markets import pricing
from oracle_voter.feeds import coinone, ukfx

WEI_VALUE = Decimal("10.0") ** -18

ABSTAIN_VOTE_PX = Decimal("-1.00").quantize(
    WEI_VALUE,
    context=Context(prec=40),
)

# Feed Sources
exchange_coinone = coinone.Coinone("https://api.coinone.co.kr")

feed_ukfx = ukfx.UKFX("https://api.ukfx.co.uk")

class ExchangeErr(Exception):
    def __init__(self, message, err):
        super().__init__(message)
        self.exchange_err = err


async def fetch_coinone_krw():
    currency = "LUNA"
    err, orderbook = await exchange_coinone.get_orderbook(currency)
    # Get MicroPrice
    if err is not None:
        raise ExchangeErr(f"Exchange Coinone threw error", err)
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
