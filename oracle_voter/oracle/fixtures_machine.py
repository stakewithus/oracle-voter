from unittest.mock import Mock, MagicMock
from decimal import Decimal, Context, getcontext
from oracle_voter.chain.mocks.fixture_utils import async_stubber, async_raiser
from oracle_voter.feeds.markets import ExchangeErr
from functools import partial
from oracle_voter.common.client import HttpError

WEI_VALUE = Decimal("10.0") ** -18

salt_mocks = {
    "18549": [
        "bfaf",
        "41a5",
        "9d6e",
        "28ef",
    ],
    "18550": [
        "ff2e",
        "2d3c",
        "1e47",
        "d534",
    ],
    "18555": [
        "3595",
        "39ff",
        "4721",
        "0c26",
    ]
}


def get_coinone():
    getcontext().prec = 6
    return async_stubber(Decimal("300.396").quantize(WEI_VALUE, context=Context(prec=40)))

def get_coinone_exception():
    return async_raiser(ExchangeErr("Coinone KRW", ""))

def not_found():
    return async_raiser(HttpError("Not found", 400, ""))

def get_rate(target):
    getcontext().prec = 6
    if target == "mnt":
        return async_stubber(Decimal(2.2575782374764977).quantize(WEI_VALUE, context=Context(prec=40)))
    if target == "usd":
        return async_stubber(Decimal(0.0008393768466290626).quantize(WEI_VALUE, context=Context(prec=40)))
    if target == "xdr":
        return async_stubber(Decimal(0.0006094236838571045).quantize(WEI_VALUE, context=Context(prec=40)))


def feed_mocks(func_coinone, func_mnt, func_usd, func_xdr):
    return [{
        "denom": "ukrw",
        "pair_type": "native",
        "markets": [{
            "exchange": "coinone",
            "feed": func_coinone,
            "weight": 100,
        }],
    }, {
        "denom": "umnt",
        "pair_type": "derivative",
        "markets": [{
            "feed": func_mnt,
            "weight": 100,
        }],
    }, {
        "denom": "uusd",
        "pair_type": "derivative",
        "markets": [{
            "feed": func_usd,
            "weight": 100,
        }],
    }, {
        "denom": "usdr",
        "pair_type": "derivative",
        "markets": [{
            "feed": func_xdr,
            "weight": 100,
        }],
    }]

def stub_oracle(height, Oracle):
    salt_mock = Mock()
    salt_mock.side_effect = salt_mocks[str(height)]
    Oracle.get_rate_salt = salt_mock
    

stub_feed_mocks_success = feed_mocks(get_coinone, partial(
    get_rate, "mnt"), partial(get_rate, "usd"), partial(get_rate, "xdr"))

stub_feed_mock_coinone_exception = feed_mocks(get_coinone_exception, partial(
    get_rate, "mnt"), partial(get_rate, "usd"), partial(get_rate, "xdr"))

stub_feed_http_error = feed_mocks(not_found, not_found, not_found, not_found)
