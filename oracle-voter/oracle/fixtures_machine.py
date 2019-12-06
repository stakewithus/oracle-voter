from functools import partial
from unittest.mock import MagicMock

from oracle.fixture_utils import (
    mock_block_data,
    mock_active_denoms,
    mock_onchain_rates,
    mock_chain_prevotes,
    mock_feed_ukfx_px,
    mock_feed_coinone_orderbook,
    mock_broadcast_tx,
)


def mock_height_18549(
    m,
    node_addr="",
    feed_coinone_url="",
    feed_ukfx_url="",
    cli_accounts=list(),
    feeder_wallet=list(),
):
    height = 18549
    validator_addr, feeder_addr = cli_accounts
    # Prepare Stubs

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
    # Mock Get Accounts
    payload = {
        "height": f"{height}",
        "result": {
            "type": "core/Account",
            "value": {
                "address": f"{feeder_addr}",
                "coins": [{
                    "denom": "uluna",
                    "amount": "100000000",
                }],
                "public_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": "AmKCbdsbJT9+JakXdH0s0c1SWuaFMpDrxLWdGRivYP6S",
                },
                "account_number": "52",
                "sequence": "77",
            }
        }
    }
    url = f"{node_addr}/auth/accounts/{feeder_addr}"
    # Sync Account #1
    m.get(url, status=200, payload=payload)
    # Sync Account #2
    m.get(url, status=200, payload=payload)

    # Mock Get Block
    stub_blockdata(
        height,
        "666880A87813145B22B0BD2EC064B652C3D94E91E6DB31BDB855CDAA88BEF7A1",
        "26339D064BF56950F46E0894FC54AAAAF83A48C10219567845D0E839B43DB0D0",
        "soju-0013",
    )

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
        [[1575541429000, 2.2575782374764977]],
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

    # Mock the POST request to broadcast
    broadcast_prevote_data = {
        "tx": signed_prevote_tx["value"],
        "mode": "sync",
    }

    stub_broadcast_tx(
        "36F6ABBE0A686D4DAC5F557EE562B421D7C47AB6DE77B986AA6D925E41645AFA",
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


def voting_e2e_3_periods(
    m,
    node_addr,
    feed_coinone_url,
    feed_ukfx_url,
    cli_accounts,
    feeder_wallet,
):
    mock_height_18549(
        m,
        node_addr,
        feed_coinone_url,
        feed_ukfx_url,
        cli_accounts,
        feeder_wallet,
    )
    """
    mock_height_18550(
        m,
        node_addr,
        feed_coinone_url,
        feed_ukfx_url,
        cli_accounts,
        feeder_wallet,
    )
    """
