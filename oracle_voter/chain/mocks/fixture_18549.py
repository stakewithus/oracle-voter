#pylint: disable-msg=too-many-arguments
from unittest.mock import MagicMock
from oracle_voter.common.util import async_stubber
from oracle_voter.chain.mocks.fixture_utils import (
    mock_account_info,
    mock_block_data,
    mock_active_denoms,
    mock_onchain_rates,
    mock_chain_prevotes,
    mock_broadcast_tx,
)

height = 18549

def account_info(feeder_addr):
    acc_pubkey = "AmKCbdsbJT9+JakXdH0s0c1SWuaFMpDrxLWdGRivYP6S"
    acc_num = "52"
    # Prepare Stubs
    return async_stubber(mock_account_info(
        feeder_addr,
        acc_pubkey,
        acc_num,
        height,
        77
    ))


def block_data():
    return async_stubber(mock_block_data(
        height,
        "666880A87813145B22B0BD2EC064B652C3D94E91E6DB31BDB855CDAA88BEF7A1",
        "26339D064BF56950F46E0894FC54AAAAF83A48C10219567845D0E839B43DB0D0",
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
            submit_hash="aebad352c771ac5797ad497043fee2c7856a6f75",
            submit_height=18547,
        ))
    if call_number == 2:
        return async_stubber(mock_chain_prevotes(
            validator_addr,
            height,
            "uusd",
            submit_hash="a883e3eb0602b0261fe7de798513d4ce478dfedc",
            submit_height=18547,
        ))
    if call_number == 3:
        return async_stubber(mock_chain_prevotes(
            validator_addr,
            height,
            "usdr",
            submit_hash="4f487244e40107f0b29211c4983de858c0f6a65f",
            submit_height=18547,
        ))
    if call_number == 4:
        return async_stubber(mock_chain_prevotes(
            validator_addr,
            height,
            "ukrw",
            submit_hash="3682c685b9130b65952f0dbd311b163fcefd247c",
            submit_height=18547,
        ))


def broadcast_tx(txhash):
    return async_stubber(mock_broadcast_tx(txhash))


def mock_height_18549(
    LCDNodeMock,
    cli_accounts=list(),
):
    validator_addr, feeder_addr = cli_accounts
    LCDNodeMock.get_account.side_effect = [
        account_info(feeder_addr), account_info(feeder_addr)]
    LCDNodeMock.get_latest_block.return_value = block_data()
    LCDNodeMock.get_oracle_active_denoms.return_value = active_denoms()
    LCDNodeMock.get_oracle_rates.return_value = onchain_rates()
    LCDNodeMock.get_oracle_prevotes_validator.side_effect = [
        chain_prevotes(validator_addr, 1),
        chain_prevotes(validator_addr, 2),
        chain_prevotes(validator_addr, 3),
        chain_prevotes(validator_addr, 4)
    ]
    LCDNodeMock.broadcast_tx_async.return_value = broadcast_tx(
        '36F6ABBE0A686D4DAC5F557EE562B421D7C47AB6DE77B986AA6D925E41645AFA')
    return LCDNodeMock
