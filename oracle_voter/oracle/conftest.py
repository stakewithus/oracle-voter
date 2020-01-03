from aioresponses import aioresponses
import pytest

from oracle_voter.chain.core import LCDNode
from oracle_voter.wallet.cli import CLIWallet

@pytest.fixture
def http_mock():
    with aioresponses() as m:
        yield m

@pytest.fixture
def node_addr():
    addr = "http://127.0.0.1:1337"
    return addr


@pytest.fixture
def feed_coinone_url():
    return "https://api.coinone.co.kr"


@pytest.fixture
def feed_ukfx_url():
    return "https://api.ukfx.co.uk"
