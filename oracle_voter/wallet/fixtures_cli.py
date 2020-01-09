import asyncio

from decimal import Decimal
from unittest.mock import PropertyMock
from oracle_voter.wallet.fixtures.offline_sign import (
    offline_sign_18549,
    offline_sign_18550,
    offline_sign_18555
)

def async_stubber(res):
    f = asyncio.Future()
    f.set_result(res)
    return f

ok_sync_state = {
    "18549": {
        "account_num": 52,
        "account_sequence": 77,
        "balance": Decimal("100.000000"),
    },
    "18550": {
        "account_num": 52,
        "account_sequence": 78,
        "balance": Decimal("100.000000"),
    },
    "18555": {
        "account_num": 52,
        "account_sequence": 79,
        "balance": Decimal("100.000000"),
    },
    "18559": {
        "account_num": 52,
        "account_sequence": 81,
        "balance": Decimal("100.000000"),
    },
}

def sync_state(height, wallet):
    w = ok_sync_state[str(height)]
    type(wallet).account_num = PropertyMock(return_value=w["account_num"]) 
    type(wallet).account_seq = PropertyMock(return_value=w["account_sequence"]) 
    type(wallet).account_balance = PropertyMock(return_value=w["balance"]) 
    return async_stubber(None)


def offline_sign(height, wallet):
    if height == 18549:
        return offline_sign_18549(wallet)
    if height == 18550:
        return offline_sign_18550(wallet)
    if height == 18555:
        return offline_sign_18555(wallet)    


def stub_wallet(height, CLIWalletMock):
    CLIWalletMock.sync_state.return_value = sync_state(height, CLIWalletMock)
    offline_sign(height, CLIWalletMock)
    return CLIWalletMock;
