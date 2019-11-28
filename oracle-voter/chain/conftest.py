import pytest

from chain.core import Transaction
from wallet.cli import CLIWallet


@pytest.fixture
def feeder_wallet():
    w = CLIWallet('oracle', '12345678')
    return w


@pytest.fixture
def tx_builder():
    return Transaction
