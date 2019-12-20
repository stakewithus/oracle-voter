from functools import partial
from unittest.mock import Mock

from oracle_voter.oracle.fixture_utils import (
    mock_account_info,
    mock_block_data,
    mock_active_denoms,
    mock_onchain_rates,
    mock_chain_prevotes,
    mock_feed_ukfx_px,
    mock_feed_coinone_orderbook,
    mock_broadcast_tx,
    mock_query_tx,
)


def mock_height_18555(
    m,
    node_addr="",
    feed_coinone_url="",
    feed_ukfx_url="",
    cli_accounts=list(),
    feeder_wallet=list(),
):
    height = 18555
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
    stub_query_tx = partial(mock_query_tx, m, node_addr)

    # Mock Get Block
    stub_blockdata(
        height,
        "92ABADC153FAE3419744FD618F6FBD2211AB34467C605D53F2D09177BA24BF6D",
        "0A47AE25572A567978F990362D13E3968A9EF147E74B22000CAFD01491558795",
        "soju-0013",
    )

    # Mock Get Tx
    stub_query_tx(
        18551,
        "36F6ABBE0A686D4DAC5F557EE562B421D7C47AB6DE77B986AA6D925E41645AFA",
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

    stub_query_tx(
        18553,
        "097817AABE904AAE1BD628487E1011FC4EF53ECD74A2D767893E5623943D1265",
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

    # Mock Get Accounts
    stub_account_info(height, 79)

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
        submit_hash="4b5117103540e7869ecc291f6a81ee27b7bf08f0",
        submit_height=18553,
    )

    stub_chain_prevotes(
        "uusd",
        submit_hash="b68ecde518d56f237bbf38e2438e5f0451520d7e",
        submit_height=18553,
    )

    stub_chain_prevotes(
        "usdr",
        submit_hash="f9cd1971df0169b59fdb4d0bccf57d1c61ac49a0",
        submit_height=18553,
    )

    stub_chain_prevotes(
        "ukrw",
        submit_hash="2cd0e2c4963b68ef880bcedd5ded8743b2dfa9dd",
        submit_height=18553,
    )
    # Mock Voting Component
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

    # feeder_wallet.offline_sign = MagicMock(return_value=signed_vote_tx)

    # Mock the POST request to broadcast
    broadcast_vote_data = {
        "tx": signed_vote_tx["value"],
        "mode": "sync",
    }

    stub_broadcast_tx(
        "4F140DBFA66D4B4B1824FE4CA2DAC77F91DD7EDB86042277F696453C37F67175",
        post_data=broadcast_vote_data,
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
        [[1575541489000, 2.2575782374764977]]
    )

    stub_feed_ukfx_px(
        "usd",
        [[1575541489000, 0.0008393768466290626]]
    )

    stub_feed_ukfx_px(
        "xdr",
        [[1575541489000, 0.0006094236838571045]]
    )

    # MagicMock the Feeder Wallet For Signing Tx

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

    #  feeder_wallet.offline_sign = MagicMock(return_value=signed_prevote_tx)
    feeder_wallet.offline_sign = Mock()
    feeder_wallet.offline_sign.side_effect = [
        signed_vote_tx,
        signed_prevote_tx,
    ]

    # Mock the POST request to broadcast
    broadcast_prevote_data = {
        "tx": signed_prevote_tx["value"],
        "mode": "sync",
    }

    stub_broadcast_tx(
        "DC9067B9291CF080CADB244B424AD7C2C05D852D49FEE65F172D3E5EFF6971EA",
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
