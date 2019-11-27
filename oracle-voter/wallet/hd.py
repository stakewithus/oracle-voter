from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.keys import HDKey, Address
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes
import base64

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

    def sign(self, data):
        priv_key = ec.derive_private_key(
            self.hd.secret,
            ec.SECP256K1(),
            default_backend(),
        )
        new_data = data.replace("\\", "a")
        nn = new_data.replace("aa", "\\")
        payload = bytes(nn, "utf-8")
        print("to bytes")
        print(payload)
        print("to bytes")
        signature = priv_key.sign(payload, ec.ECDSA(hashes.SHA256()))
        r, s = utils.decode_dss_signature(signature)
        # final_sig = r | s
        # print(final_sig)
        # print(final_sig.to_bytes(32, byteorder="big"))
        final_sig = r.to_bytes(32, byteorder="little") + s.to_bytes(32, byteorder="little")
        print('Sig Bytes before encode')
        print(final_sig)
        print('Sig Bytes before encode')
        print("What we should get")
        print("SfNv0+GCQTw48YPZLrFVeCp4mdF0G5SwL6M9Rqzp4IZQE8JKqulN8cEIplFGhGeEGodgaZxIseLRxC6OUScNPw==")
        real_sig_b = base64.b64decode(bytes("SfNv0+GCQTw48YPZLrFVeCp4mdF0G5SwL6M9Rqzp4IZQE8JKqulN8cEIplFGhGeEGodgaZxIseLRxC6OUScNPw==", "ascii"))
        print(real_sig_b)
        real_r = real_sig_b[0:32]
        real_s = real_sig_b[32:]
        print(real_r)
        print(len(real_r))
        print(real_s)
        print(len(real_s))
        real_DER = utils.encode_dss_signature(int.from_bytes(real_r, "big"), int.from_bytes(real_s, "big"))
        print("REAL DER")
        print(real_DER)
        # Verfy with Public Key
        verify_payload = b'{"account_number": "45", "chain_id": "soju-0012", "fee": {"amount": [], "gas": "200000"}, "memo": "", "msgs": [{"type": "oracle\\/MsgExchangeRateVote", "value": {"denom": "ukrw", "exchange_rate": "8000.000000000000000000", "feeder": "terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm", "salt": "1234", "validator": "terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu"}}], "sequence": "0"}'
        print(verify_payload)

        priv_key.public_key().verify(real_DER, verify_payload, ec.ECDSA(hashes.SHA256()))

        print(len(real_sig_b))
        print("End")
        return signature


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
