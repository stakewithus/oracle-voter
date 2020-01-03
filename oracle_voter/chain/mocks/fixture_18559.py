#pylint: disable-msg=too-many-arguments
from unittest.mock import MagicMock

from oracle_voter.chain.mocks.fixture_utils import (
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


async def account_info(feeder_addr):
    acc_pubkey = "AmKCbdsbJT9+JakXdH0s0c1SWuaFMpDrxLWdGRivYP6S"
    acc_num = "52"
    # Prepare Stubs
    return mock_account_info(
        feeder_addr,
        acc_pubkey,
        acc_num,
        height,
        79
    )


async def block_data():
    return mock_block_data(
        height,
        "9DDE2673138D3F98313144D6D6167F5FA0D86969CF183C63D453C1A763C833E1",
        "B2951BFC41D220588777428E6CD6F8D4664EAA9044DEC73EDE569EF2D3893DB1",
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
            submit_hash="4b5117103540e7869ecc291f6a81ee27b7bf08f0",
            submit_height=18553,
        )
    if call_number == 2:
        return mock_chain_prevotes(
            validator_addr,
            height,
            "uusd",
            submit_hash="b68ecde518d56f237bbf38e2438e5f0451520d7e",
            submit_height=18553,
        )
    if call_number == 3:
        return mock_chain_prevotes(
            validator_addr,
            height,
            "usdr",
            submit_hash="f9cd1971df0169b59fdb4d0bccf57d1c61ac49a0",
            submit_height=18553,
        )
    if call_number == 4:
        return mock_chain_prevotes(
            validator_addr,
            height,
            "ukrw",
            submit_hash="2cd0e2c4963b68ef880bcedd5ded8743b2dfa9dd",
            submit_height=18553,
        )


async def broadcast_tx(txhash):
    return mock_broadcast_tx(txhash)


async def query_tx(txhash):
    return mock_query_tx(height, txhash)


def mock_height_18559(
    http_mock,
    feed_coinone_url="",
    feed_ukfx_url="",
    cli_accounts=list(),
    LCDNodeMock=object
):
    validator_addr, feeder_addr = cli_accounts
    mock_init(http_mock, feed_coinone_url, feed_ukfx_url)
    lcd_node = LCDNodeMock.return_value
    lcd_node.get_account.side_effect = [account_info(feeder_addr)]
    lcd_node.get_latest_block.return_value = block_data()
    lcd_node.get_oracle_active_denoms.return_value = active_denoms()
    lcd_node.get_oracle_rates.return_value = onchain_rates()
    lcd_node.get_oracle_prevotes_validator.side_effect = [
        chain_prevotes(validator_addr, 1),
        chain_prevotes(validator_addr, 2),
        chain_prevotes(validator_addr, 3),
        chain_prevotes(validator_addr, 4)
    ]
    lcd_node.broadcast_tx_async.return_value = broadcast_tx(
        '4F140DBFA66D4B4B1824FE4CA2DAC77F91DD7EDB86042277F696453C37F67175')

    return lcd_node
