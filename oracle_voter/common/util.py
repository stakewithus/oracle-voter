import asyncio
from oracle_voter.common.client import HttpError

def async_stubber(res):
    f = asyncio.Future()
    f.set_result(res)
    return f


def async_raiser(err):
    f = asyncio.Future()
    f.set_exception(err)
    return f


def not_found():
    return async_raiser(HttpError("Not found", 400, ""))
