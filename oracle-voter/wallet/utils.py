from enum import Enum
import bech32


class AccountEnum(Enum):
    ADDRESS = 1
    PUBKEY_ED25519 = 2
    PUBKEY_SECP256K1 = 3


types_padding = {
    AccountEnum.ADDRESS: "",
    AccountEnum.PUBKEY_SECP256K1: "eb5ae98721",
}


def bech32ify(account_type, hrp, hash_data):
    total_data = f"{types_padding[account_type]}{hash_data}"
    b_range = range(0, len(total_data), 2)
    b = [
        f"{total_data[i]}{total_data[i+1]}" for i in b_range
    ]
    bb = [int(x, 16) for x in b]
    data = bech32.convertbits(bb, 8, 5)
    return bech32.bech32_encode(hrp, data)
