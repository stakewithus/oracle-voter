from aioresponses import aioresponses
import pytest
from chain.core import LCDNode
from wallet.cli import CLIWallet


@pytest.fixture
def http_mock():
    with aioresponses() as m:
        yield m


@pytest.fixture
def cli_accounts():
    return (
        "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9",
        "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y"
    )


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


@pytest.fixture
def lcd_node(node_addr):
    n = LCDNode(addr=node_addr)
    return n


@pytest.fixture
def feeder_wallet(cli_accounts, lcd_node):
    account_addr = cli_accounts[1]
    w = CLIWallet(
        "feeder",
        "12345678",
        account_addr,
        lcd_node=lcd_node,
    )
    return w
