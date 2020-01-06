from unittest.mock import MagicMock, Mock

def offline_sign_18549(feeder_wallet):
    signed_prevote_tx = {
        "type": "core/StdTx",
        "value": {
            "msg": [{
                "type": "oracle/MsgExchangeRatePrevote",
                "value": {
                    "hash": "af84810bd284e77afb55c2d68df5abdbceb5a357",
                    "denom": "ukrw",
                    "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                    "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9",
                }
            }, {
                "type": "oracle/MsgExchangeRatePrevote",
                "value": {
                    "hash": "841b1c093ecf481b60f69dd55f51d25f110ece20",
                    "denom": "umnt",
                    "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                    "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9",
                }
            }, {
                "type": "oracle/MsgExchangeRatePrevote",
                "value": {
                    "hash": "6ba91d17d16914659af76756b6d9ba8b27685b69",
                    "denom": "usdr",
                    "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                    "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9",
                },
            }, {
                "type": "oracle/MsgExchangeRatePrevote",
                "value": {
                    "hash": "c38a970c4b0c548df321bd38db8cb704f180725b",
                    "denom": "uusd",
                    "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                    "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9",
                },
            }],
            "fee": {"amount": [], "gas": "200000"},
            "signatures": [{
                "pub_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": "AmKCbdsbJT9+JakXdH0s0c1SWuaFMpDrxLWdGRivYP6S",
                },
                "signature": "A3VgQndG5CWo/so4wNs6kMqP1pA3ChhQiiuivlX/G2xgwVQr8g4LaMigedorKGE3+SG3Qq2P29wx/bP8ebrqzg==",
            }
            ],
            "memo": "",
        }
    }

    feeder_wallet.offline_sign = MagicMock(return_value=signed_prevote_tx)


def offline_sign_18550(feeder_wallet):
    signed_prevote_tx = {
        "type": "core/StdTx",
        "value": {
            "msg": [{
                "type": "oracle/MsgExchangeRatePrevote",
                "value": {
                    "hash": "2cd0e2c4963b68ef880bcedd5ded8743b2dfa9dd",
                    "denom": "ukrw",
                    "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                    "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9",
                }
            }, {
                "type": "oracle/MsgExchangeRatePrevote",
                "value": {
                    "hash": "4b5117103540e7869ecc291f6a81ee27b7bf08f0",
                    "denom": "umnt",
                    "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                    "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9",
                },
            }, {
                "type": "oracle/MsgExchangeRatePrevote",
                "value": {
                    "hash": "f9cd1971df0169b59fdb4d0bccf57d1c61ac49a0",
                    "denom": "usdr",
                    "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                    "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9",
                },
            }, {
                "type": "oracle/MsgExchangeRatePrevote",
                "value": {
                    "hash": "b68ecde518d56f237bbf38e2438e5f0451520d7e",
                    "denom": "uusd",
                    "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                    "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9",
                }
            }],
            "fee": {"amount": [], "gas": "200000"},
            "signatures": [{
                "pub_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": "AmKCbdsbJT9+JakXdH0s0c1SWuaFMpDrxLWdGRivYP6S",
                },
                "signature": "ymPLeIM7wqNsdgnwECgG7apfJ/p5DkX7Q8j0OEvirUNctO3aL3IDWd+F7/ovN4tTjFaG8OY5G9yr6VLaSapXwA=="
            }],
            "memo": "",
        }
    }

    feeder_wallet.offline_sign = MagicMock(return_value=signed_prevote_tx)


def offline_sign_18555(feeder_wallet):
    signed_vote_tx = {
        "type": "core/StdTx",
        "value": {
            "msg": [
                {
                    "type": "oracle/MsgExchangeRateVote",
                    "value": {
                        "exchange_rate": "300.396000000000000000",
                        "salt": "ff2e",
                        "denom": "ukrw",
                        "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                        "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9"
                    }
                },
                {
                    "type": "oracle/MsgExchangeRateVote",
                    "value": {
                        "exchange_rate": "678.168000000000000000",
                        "salt": "2d3c",
                        "denom": "umnt",
                        "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                        "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9"
                    }
                },
                {
                    "type": "oracle/MsgExchangeRateVote",
                    "value": {
                        "exchange_rate": "0.183069000000000000",
                        "salt": "1e47",
                        "denom": "usdr",
                        "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                        "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9"
                    }
                },
                {
                    "type": "oracle/MsgExchangeRateVote",
                    "value": {
                        "exchange_rate": "0.252145000000000000",
                        "salt": "d534",
                        "denom": "uusd",
                        "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                        "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9"
                    }
                }
            ],
            "signatures": [{
                "pub_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": "AmKCbdsbJT9+JakXdH0s0c1SWuaFMpDrxLWdGRivYP6S",
                },
                "signature": "kYxxk67pz+bBg1+NWQcmPs+FZlXHIPhqfdRcvG/Io1dJeGTGRPRlKN8j5RK4LYKLQNNcRh42517/nkBwzft1tQ==",
            }],
            "fee": {"amount": [], "gas": "200000"},
            "memo": "",
        }
    }
    signed_prevote_tx = {
        "type": "core/StdTx",
        "value": {
            "msg": [{
                "type": "oracle/MsgExchangeRatePrevote",
                "value": {
                    "hash": "281f936e1bc1e2108c76d5120d9ec789533926b8",
                    "denom": "ukrw",
                    "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                    "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9"
                }
            }, {
                "type": "oracle/MsgExchangeRatePrevote",
                "value": {
                    "hash": "fd8fd834f013248aa9faf88d628c173dd47df263",
                    "denom": "umnt",
                    "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                    "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9"
                }
            }, {
                "type": "oracle/MsgExchangeRatePrevote",
                "value": {
                    "hash": "826c89b1bbcd31a96a107dbedf3de624a9dd3daf",
                    "denom": "usdr",
                    "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                    "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9"
                }
            }, {
                "type": "oracle/MsgExchangeRatePrevote",
                "value": {
                    "hash": "a3988e119ae62e0018ad0603e198b915b08a7749",
                    "denom": "uusd",
                    "feeder": "terra1pwm7nz0nt7kz45rm0x7jq0qhm6sl4t0ukpvk3y",
                    "validator": "terravaloper1rhrptnx87ufpv62c7ngt9yqlz2hr77xr9nkcr9"
                }
            }],
            "fee": {
                "amount": [],
                "gas": "200000"
            },
            "memo": "",
            "signatures": [{
                "pub_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": "AmKCbdsbJT9+JakXdH0s0c1SWuaFMpDrxLWdGRivYP6S",
                },
                "signature": "nn1jqMkBpsbhkM64g43PTj56rCQUBf6psToebobKTItFxm7Pmi04tGmXyBfiZ05pet1yo9O1vtMRY5iFatI8sg==",
            }],
        }
    }

    feeder_wallet.offline_sign = Mock()
    feeder_wallet.offline_sign.side_effect = [
        signed_vote_tx,
        signed_prevote_tx,
    ]

