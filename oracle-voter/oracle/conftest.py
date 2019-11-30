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
        "terravaloper1emscfpz9jjtj8tj2nh70y25uywcakldsj76luz",
        "terra1pmx2lh86zs9cgms549dwrdca3nycedde4enl7x"
    )


@pytest.fixture
def node_addr():
    addr = "http://127.0.0.1:1337"
    return addr


@pytest.fixture
def lcd_node(node_addr):
    n = LCDNode(addr=node_addr)
    return n


@pytest.fixture
def feeder_wallet(lcd_node):
    w = CLIWallet(
        "feeder",
        "12345678",
        lcd_node=lcd_node,
    )
    return w
