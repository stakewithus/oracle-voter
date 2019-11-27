import pytest
from wallet.fixtures_hd import get_seed_phrase_1, get_seed_phrase_2


def test_hd_wallet_init_fail(hd_wallet):
    with pytest.raises(ValueError):
        input_phrase = "hello world"
        hd_wallet.import_from_seed_phrase(input_phrase)


def test_hd_wallet_init_pass(hd_wallet):
    master_wallet = hd_wallet.import_from_seed_phrase(get_seed_phrase_1())
    tw = master_wallet.get_account(
        coin=330,
        hrp_pubkey="terrapub",
        hrp_address="terra",
    )
    assert tw.local_address == "terra1twqxu3f7zgxmxmfs8ytvnkkgzd4cpndjq8ls89"
    pk = "terrapub1addwnpepqgt6an47sd7kvhz0dnzt9x02at07xhkfx4xspuqz54pu85hfm0aqy8z786q"
    assert tw.local_pubkey == pk


def test_hd_wallet_init_pass_2(hd_wallet):
    master_wallet = hd_wallet.import_from_seed_phrase(get_seed_phrase_2())
    tw = master_wallet.get_account(
        coin=330,
        hrp_pubkey="terrapub",
        hrp_address="terra",
    )
    assert tw.local_address == "terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm"
    pk = "terrapub1addwnpepqtxfw868a4vsm02mrnsv9974m938hqju5kq0nk3c7awqru7slpw2g8cvhuy"
    assert tw.local_pubkey == pk
