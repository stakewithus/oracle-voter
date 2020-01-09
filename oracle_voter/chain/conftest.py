import pytest
from decimal import Decimal

from oracle_voter.chain.core import Transaction
from oracle_voter.wallet.cli import CLIWallet
from oracle_voter.config.test_settings import get_settings
import os
from os.path import join, dirname

test_settings = get_settings()
@pytest.fixture
def account_addrs():
    return (
        test_settings.get('oracle_addr'),  # Feeder
        test_settings.get('oracle_validator_addr'),
    )


@pytest.fixture
def sign_data():
    return (test_settings.get('chain_test_public_key'), test_settings.get('chain_test_signature'))


@pytest.fixture
def feeder_wallet(account_addrs):
    feeder_addr = account_addrs[0]
    w = CLIWallet(
        test_settings.get('oracle_account'),
        test_settings.get('oracle_pw'),
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
