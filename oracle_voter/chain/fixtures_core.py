import asyncio

from oracle_voter.chain.mocks.fixture_utils import (
    mock_block_data as stub_block_data,
)

def async_stubber(res):
    f = asyncio.Future()
    f.set_result(res)
    return f

ok_latest_block = {
    "18549": stub_block_data(
        18549,
        "666880A87813145B22B0BD2EC064B652C3D94E91E6DB31BDB855CDAA88BEF7A1",
        "26339D064BF56950F46E0894FC54AAAAF83A48C10219567845D0E839B43DB0D0",
        "soju-0013",
    ),
}


def get_latest_block(height, opts = dict()):
    return async_stubber(ok_latest_block[str(height)])
