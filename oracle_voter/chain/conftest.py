import pytest
from decimal import Decimal

from oracle_voter.chain.core import Transaction
from oracle_voter.wallet.cli import CLIWallet

import os
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv()

a = os.environ.get('FEEDER_ADDRESS')
@pytest.fixture
def account_addrs():
    return (
        os.environ.get('FEEDER_ADDRESS'),
        os.environ.get('VALIDATOR_ADDRESS'))
    # return (
    #     "terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm",  # Feeder
    #     "terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",  # Validator
    # )


@pytest.fixture
def sign_data():
    return (os.environ.get('PUBLIC_KEY'), os.environ.get('SIGNATURE'))
    #return ("AsyXH0ftWQ29WxzgwpfV2WJ7glylgPnaOPdcAfPQ+Fyk", "ZOI24iYEoW4GmMCIaFvoCjSoBO1fZyuryaOwjaNavzYAjK9ebgs1PLkD6hhlZ7umIRCvLhNTZkspoEwKM1w/UQ==")


@pytest.fixture
def feeder_wallet(account_addrs):
    feeder_addr = account_addrs[0]
    w = CLIWallet(
        'oracle',
        os.environ.get('ACCOUNT_PASSWORD'),
        #'12345678',
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
