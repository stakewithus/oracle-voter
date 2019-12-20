from functools import partial
from unittest.mock import MagicMock

from oracle_voter.oracle.fixture_utils import (
    mock_account_info,
    mock_block_data,
    mock_active_denoms,
    mock_onchain_rates,
    mock_chain_prevotes,
    mock_feed_ukfx_px,
    mock_feed_coinone_orderbook,
    mock_broadcast_tx,
)


def mock_height_18550(
    m,
    node_addr="",
    feed_coinone_url="",
    feed_ukfx_url="",
    cli_accounts=list(),
    feeder_wallet=list(),
):
    height = 18550
    validator_addr, feeder_addr = cli_accounts
    acc_pubkey = "AmKCbdsbJT9+JakXdH0s0c1SWuaFMpDrxLWdGRivYP6S"
    acc_num = "52"
    # Prepare Stubs
    stub_account_info = partial(
        mock_account_info,
        m,
        node_addr,
        feeder_addr,
        acc_pubkey,
        acc_num,
    )
    stub_blockdata = partial(mock_block_data, m, node_addr)
    stub_active_denoms = partial(mock_active_denoms, m, node_addr, height)
    stub_onchain_rates = partial(mock_onchain_rates, m, node_addr, height)
    stub_chain_prevotes = partial(
        mock_chain_prevotes,
        m,
        node_addr,
        validator_addr,
        height,
    )
    stub_feed_coinone_orderbook = partial(
        mock_feed_coinone_orderbook,
        m,
        feed_coinone_url,
    )
    stub_feed_ukfx_px = partial(
        mock_feed_ukfx_px,
        m,
        feed_ukfx_url,
    )
    stub_broadcast_tx = partial(mock_broadcast_tx, m, node_addr)

    # Mock Get Block
    stub_blockdata(
        height,
        "C0006E180BA9BFAAD01020477E7CD8A45A4B428684C69D2992E57887715479EE",
        "666880A87813145B22B0BD2EC064B652C3D94E91E6DB31BDB855CDAA88BEF7A1",
        "soju-0013",
    )

    # Mock Get Accounts
    stub_account_info(height, 77)

    # Mock Active Denoms
    stub_active_denoms()

    # Mock Exchange Rates On-Chain
    stub_onchain_rates(
        ukrw="300.000000000000000000",
        umnt="684.542466258089234543",
        usdr="0.182737050935369655",
        uusd="0.251817321037518416",
    )

    # Stub OnChain Prevotes
    stub_chain_prevotes(
        "umnt",
        submit_hash="aebad352c771ac5797ad497043fee2c7856a6f75",
        submit_height=18547,
    )

    stub_chain_prevotes(
        "uusd",
        submit_hash="a883e3eb0602b0261fe7de798513d4ce478dfedc",
        submit_height=18547,
    )

    stub_chain_prevotes(
        "usdr",
        submit_hash="4f487244e40107f0b29211c4983de858c0f6a65f",
        submit_height=18547,
    )

    stub_chain_prevotes(
        "ukrw",
        submit_hash="3682c685b9130b65952f0dbd311b163fcefd247c",
        submit_height=18547,
    )

    # Mock Luna Orderbook
    stub_feed_coinone_orderbook(
        "LUNA",
        [
            {"price": "301.0", "qty": "1902.6306"},
            {"price": "302.0", "qty": "1861.4027"},
            {"price": "303.0", "qty": "200.0"},
        ],
        [
            {"price": "299.0", "qty": "641.5213"},
            {"price": "298.0", "qty": "1071.129"},
            {"price": "297.0", "qty": "2.0"},
        ],
    )

    stub_feed_ukfx_px(
        "mnt",
        [[1575541429000, 2.2575782374764977]]
    )

    stub_feed_ukfx_px(
        "usd",
        [[1575541429000, 0.0008393768466290626]]
    )

    stub_feed_ukfx_px(
        "xdr",
        [[1575541429000, 0.0006094236838571045]]
    )

    # MagicMock the Feeder Wallet For Signing Tx
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

    # Mock the POST request to broadcast
    broadcast_prevote_data = {
        "tx": signed_prevote_tx["value"],
        "mode": "sync",
    }

    stub_broadcast_tx(
        "097817AABE904AAE1BD628487E1011FC4EF53ECD74A2D767893E5623943D1265",
        post_data=broadcast_prevote_data,
        logs=[{
            "msg_index": 0,
            "success": True,
            "log": "",
        }, {
            "msg_index": 1,
            "success": True,
            "log": "",
        }, {
            "msg_index": 2,
            "success": True,
            "log": "",
        }, {
            "msg_index": 3,
            "success": True,
            "log": "",
        }],
    )
