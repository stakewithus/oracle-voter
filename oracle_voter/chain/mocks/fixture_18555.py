#pylint: disable-msg=too-many-arguments
from unittest.mock import MagicMock

from oracle_voter.chain.mocks.fixture_utils import (
    async_stubber,
    mock_account_info,
    mock_block_data,
    mock_active_denoms,
    mock_onchain_rates,
    mock_chain_prevotes,
    mock_broadcast_tx,
    mock_query_tx,
)
from oracle_voter.chain.mocks.fixture_market import mock_init
height = 18555


def account_info(feeder_addr):
    acc_pubkey = "AmKCbdsbJT9+JakXdH0s0c1SWuaFMpDrxLWdGRivYP6S"
    acc_num = "52"
    # Prepare Stubs
    return async_stubber(mock_account_info(
        feeder_addr,
        acc_pubkey,
        acc_num,
        height,
        79
    ))


def block_data():
    return async_stubber(mock_block_data(
        height,
        "92ABADC153FAE3419744FD618F6FBD2211AB34467C605D53F2D09177BA24BF6D",
        "0A47AE25572A567978F990362D13E3968A9EF147E74B22000CAFD01491558795",
        "soju-0013",
    ))


def active_denoms():
    return async_stubber(mock_active_denoms(height))


def onchain_rates():
    return async_stubber(mock_onchain_rates(
        height,
        ukrw="300.000000000000000000",
        umnt="684.542466258089234543",
        usdr="0.182737050935369655",
        uusd="0.251817321037518416",
    ))


def chain_prevotes(validator_addr, call_number):
    if call_number == 1:
        return async_stubber(mock_chain_prevotes(
            validator_addr,
            height,
            "umnt",
            submit_hash="4b5117103540e7869ecc291f6a81ee27b7bf08f0",
            submit_height=18553,
        ))
    if call_number == 2:
        return async_stubber(mock_chain_prevotes(
            validator_addr,
            height,
            "uusd",
            submit_hash="b68ecde518d56f237bbf38e2438e5f0451520d7e",
            submit_height=18553,
        ))
    if call_number == 3:
        return async_stubber(mock_chain_prevotes(
            validator_addr,
            height,
            "usdr",
            submit_hash="f9cd1971df0169b59fdb4d0bccf57d1c61ac49a0",
            submit_height=18553,
        ))
    if call_number == 4:
        return async_stubber(mock_chain_prevotes(
            validator_addr,
            height,
            "ukrw",
            submit_hash="2cd0e2c4963b68ef880bcedd5ded8743b2dfa9dd",
            submit_height=18553,
        ))


def broadcast_tx(txhash):
    return async_stubber(mock_broadcast_tx(txhash))

def query_tx(height, txhash):
    return async_stubber(mock_query_tx(height, txhash))

def mock_height_18555(
    LCDNodeMock,
    cli_accounts=list(),
):
    validator_addr, feeder_addr = cli_accounts
    LCDNodeMock.get_account.side_effect = [account_info(feeder_addr)]
    LCDNodeMock.get_latest_block.return_value = block_data()
    LCDNodeMock.get_oracle_active_denoms.return_value = active_denoms()
    LCDNodeMock.get_oracle_rates.return_value = onchain_rates()
    LCDNodeMock.get_oracle_prevotes_validator.side_effect = [
        chain_prevotes(validator_addr, 1),
        chain_prevotes(validator_addr, 2),
        chain_prevotes(validator_addr, 3),
        chain_prevotes(validator_addr, 4)
    ]
    LCDNodeMock.broadcast_tx_async.side_effect = [
        broadcast_tx('4F140DBFA66D4B4B1824FE4CA2DAC77F91DD7EDB86042277F696453C37F67175'),
        broadcast_tx('DC9067B9291CF080CADB244B424AD7C2C05D852D49FEE65F172D3E5EFF6971EA')
    ]
    LCDNodeMock.get_tx.side_effect = [
        query_tx(18551, '36F6ABBE0A686D4DAC5F557EE562B421D7C47AB6DE77B986AA6D925E41645AFA'),
        query_tx(18553, '097817AABE904AAE1BD628487E1011FC4EF53ECD74A2D767893E5623943D1265')
    ]
    return LCDNodeMock
