import pytest
from wallet.hd import HDWallet


@pytest.fixture
def hd_wallet():
    return HDWallet
