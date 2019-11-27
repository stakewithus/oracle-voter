from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.keys import HDKey, Address

from wallet.utils import bech32ify, AccountEnum


class HDAccount:

    def __init__(self, hd, hrp_pubkey="", hrp_address=""):
        self.hd = hd
        addr = Address(hd.public_hex, script_type="p2pkh")
        self.local_address = bech32ify(
            AccountEnum.ADDRESS,
            hrp_address,
            addr.hashed_data,
        )
        self.local_pubkey = bech32ify(
            AccountEnum.PUBKEY_SECP256K1,
            hrp_pubkey,
            hd.public_hex
        )
        # Get the Hash Of the Address


class HDWallet:

    def __init__(self, seed):
        self.master_hd = HDKey.from_seed(seed)

    def get_account(
        self,
        coin=0,
        account=0,
        change=0,
        address_idx=0,
        hrp_pubkey="",
        hrp_address="",
    ):
        hd_path = f"m/44'/{coin}'/{account}'/{change}/{address_idx}"
        new_hd = self.master_hd.subkey_for_path(hd_path)
        return HDAccount(
            new_hd,
            hrp_pubkey=hrp_pubkey,
            hrp_address=hrp_address,
        )

    @staticmethod
    def import_from_seed_phrase(input_phrase):
        # Raises a ValueError if input_phrase is invalid
        seed = Mnemonic().to_seed(input_phrase)
        return HDWallet(seed)
