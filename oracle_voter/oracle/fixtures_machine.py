from unittest.mock import Mock, MagicMock
from decimal import Decimal, Context, getcontext
from oracle_voter.chain.mocks.fixture_utils import async_stubber
from functools import partial

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


def get_rate(target):
    getcontext().prec = 6
    if target == "mnt":
        return async_stubber(Decimal(2.2575782374764977).quantize(WEI_VALUE, context=Context(prec=40)))
    if target == "usd":
        return async_stubber(Decimal(0.0008393768466290626).quantize(WEI_VALUE, context=Context(prec=40)))
    if target == "xdr":
        return async_stubber(Decimal(0.0006094236838571045).quantize(WEI_VALUE, context=Context(prec=40)))


feed_mocks = [{
    "denom": "ukrw",
    "pair_type": "native",
    "markets": [{
        "exchange": "coinone",
        "feed": get_coinone,
        "weight": 100,
    }],
}, {
    "denom": "umnt",
    "pair_type": "derivative",
    "markets": [{
        "feed": partial(get_rate, "mnt"),
        "weight": 100,
    }],
}, {
    "denom": "uusd",
    "pair_type": "derivative",
    "markets": [{
        "feed": partial(get_rate, "usd"),
        "weight": 100,
    }],
}, {
    "denom": "usdr",
    "pair_type": "derivative",
    "markets": [{
        "feed": partial(get_rate, "xdr"),
        "weight": 100,
    }],
}]

def stub_oracle(height, Oracle):
    salt_mock = Mock()
    salt_mock.side_effect = salt_mocks[str(height)]
    Oracle.get_rate_salt = salt_mock
    
