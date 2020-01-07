import asyncio

from decimal import Decimal
from unittest.mock import PropertyMock

def async_stubber(res):
    f = asyncio.Future()
    f.set_result(res)
    return f

ok_sync_state = {
    "18549": {
        "account_num": 52,
        "account_sequence": 77,
        "balance": Decimal("1000.00"),
    },
}

def sync_state(height, wallet):
    w = ok_sync_state[str(height)]
    type(wallet).account_num = PropertyMock(return_value=w["account_num"]) 
    type(wallet).account_seq = PropertyMock(return_value=w["account_sequence"]) 
    type(wallet).account_balance = PropertyMock(return_value=w["balance"]) 
    return async_stubber(None)
