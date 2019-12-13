import pytest

from chain.core import Transaction
from wallet.cli import CLIWallet
from decimal import Decimal


@pytest.fixture
def account_addrs():
    return (
        "terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm",  # Feeder
        "terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",  # Validator
    )


@pytest.fixture
def feeder_wallet(account_addrs):
    feeder_addr = account_addrs[0]
    w = CLIWallet(
        'oracle',
        '12345678',
        feeder_addr,
    )
    return w


@pytest.fixture
def tx_builder():
    return Transaction


@pytest.fixture
def wei_value():
    EIGHTEEN_PLACES = Decimal(10) ** -18
    return EIGHTEEN_PLACES
