#pylint: disable-msg=too-many-arguments
from unittest.mock import MagicMock
from oracle_voter.common.client import HttpError

from oracle_voter.chain.mocks.fixture_utils import (
    mock_account_info,
    mock_block_data,
    mock_active_denoms,
    mock_onchain_rates,
    mock_chain_prevotes,
    mock_broadcast_tx,
    mock_query_tx,
    mock_query_tx
)
from oracle_voter.chain.mocks.fixture_market import mock_init
height = 18550


async def account_info(feeder_addr):
    acc_pubkey = "AmKCbdsbJT9+JakXdH0s0c1SWuaFMpDrxLWdGRivYP6S"
    acc_num = "52"
    # Prepare Stubs
    return mock_account_info(
        feeder_addr,
        acc_pubkey,
        acc_num,
        height,
        77
    )


async def block_data():
    return mock_block_data(
        height,
        "C0006E180BA9BFAAD01020477E7CD8A45A4B428684C69D2992E57887715479EE",
        "666880A87813145B22B0BD2EC064B652C3D94E91E6DB31BDB855CDAA88BEF7A1",
        "soju-0013",
    )


async def active_denoms():
    return mock_active_denoms(height)


async def onchain_rates():
    return mock_onchain_rates(
        height,
        ukrw="300.000000000000000000",
        umnt="684.542466258089234543",
        usdr="0.182737050935369655",
        uusd="0.251817321037518416",
    )


async def chain_prevotes(validator_addr, call_number):
    if call_number == 1:
        return mock_chain_prevotes(
            validator_addr,
            height,
            "umnt",
            submit_hash="aebad352c771ac5797ad497043fee2c7856a6f75",
            submit_height=18547,
        )
    if call_number == 2:
        return mock_chain_prevotes(
            validator_addr,
            height,
            "uusd",
            submit_hash="a883e3eb0602b0261fe7de798513d4ce478dfedc",
            submit_height=18547,
        )
    if call_number == 3:
        return mock_chain_prevotes(
            validator_addr,
            height,
            "usdr",
            submit_hash="4f487244e40107f0b29211c4983de858c0f6a65f",
            submit_height=18547,
        )
    if call_number == 4:
        return mock_chain_prevotes(
            validator_addr,
            height,
            "ukrw",
            submit_hash="3682c685b9130b65952f0dbd311b163fcefd247c",
            submit_height=18547,
        )


async def broadcast_tx(txhash):
    return mock_broadcast_tx(txhash)


async def query_tx():
    raise HttpError('Connection error', '400', '')


def mock_height_18550(
    http_mock,
    feed_coinone_url="",
    feed_ukfx_url="",
    cli_accounts=list(),
    lcd_node=object
):
    validator_addr, feeder_addr = cli_accounts
    mock_init(http_mock, feed_coinone_url, feed_ukfx_url)
    lcd_node.get_account.side_effect = [
        account_info(feeder_addr)]
    lcd_node.get_latest_block.return_value = block_data()
    lcd_node.get_oracle_active_denoms.return_value = active_denoms()
    lcd_node.get_oracle_rates.return_value = onchain_rates()
    lcd_node.get_oracle_prevotes_validator.side_effect = [
        chain_prevotes(validator_addr, 1),
        chain_prevotes(validator_addr, 2),
        chain_prevotes(validator_addr, 3),
        chain_prevotes(validator_addr, 4)
    ]
    txhash = '097817AABE904AAE1BD628487E1011FC4EF53ECD74A2D767893E5623943D1265'
    lcd_node.broadcast_tx_async.return_value = broadcast_tx(txhash)
    lcd_node.get_tx.return_value = query_tx()
    return lcd_node
