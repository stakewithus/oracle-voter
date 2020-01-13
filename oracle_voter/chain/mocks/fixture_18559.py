#pylint: disable-msg=too-many-arguments
from unittest.mock import MagicMock
from oracle_voter.common.util import async_stubber
from oracle_voter.chain.mocks.fixture_utils import (
    mock_account_info,
    mock_block_data,
    mock_query_tx,
)
height = 18559


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
        "9DDE2673138D3F98313144D6D6167F5FA0D86969CF183C63D453C1A763C833E1",
        "B2951BFC41D220588777428E6CD6F8D4664EAA9044DEC73EDE569EF2D3893DB1",
        "soju-0013",
    ))


def query_tx(height, txhash):
    return async_stubber(mock_query_tx(height, txhash))


def mock_height_18559(
    LCDNodeMock,
    cli_accounts=list(),
):
    _, feeder_addr = cli_accounts
    LCDNodeMock.get_account.side_effect = [account_info(feeder_addr)]
    LCDNodeMock.get_latest_block.return_value = block_data()
    LCDNodeMock.get_tx.side_effect = [
        query_tx(
            18557, '4F140DBFA66D4B4B1824FE4CA2DAC77F91DD7EDB86042277F696453C37F67175'),
        query_tx(
            18557, 'DC9067B9291CF080CADB244B424AD7C2C05D852D49FEE65F172D3E5EFF6971EA')
    ]
    return LCDNodeMock
