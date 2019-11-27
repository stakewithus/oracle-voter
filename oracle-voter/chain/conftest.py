import pytest
from wallet.hd import HDWallet
from wallet.fixtures_hd import get_seed_phrase_2

from chain.core import Transaction


@pytest.fixture
def feeder_wallet():
    master_wallet = HDWallet.import_from_seed_phrase(get_seed_phrase_2())
    tw = master_wallet.get_account(
        coin=330,
        hrp_pubkey="terrapub",
        hrp_address="terra",
    )
    return tw


@pytest.fixture
def tx_builder():
    return Transaction
