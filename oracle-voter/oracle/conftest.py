from aioresponses import aioresponses
import pytest


@pytest.fixture
def http_mock():
    with aioresponses() as m:
        yield m


@pytest.fixture
def node_addr():
    return "http://127.0.0.1:1337"


@pytest.fixture
def validator_addr():
    return "terravaloper1emscfpz9jjtj8tj2nh70y25uywcakldsj76luz"


@pytest.fixture
def feeder_addr():
    return "terra1pmx2lh86zs9cgms549dwrdca3nycedde4enl7x"


@pytest.fixture
def wallet_name():
    return "feeder"


@pytest.fixture
def wallet_password():
    return "12345678"
