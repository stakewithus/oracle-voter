from functools import partial

from oracle.fixture_utils import (
    mock_account_info,
    mock_block_data,
    mock_query_tx,
)


def mock_height_18559(
    m,
    node_addr="",
    feed_coinone_url="",
    feed_ukfx_url="",
    cli_accounts=list(),
    feeder_wallet=list(),
):
    height = 18559
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
    stub_query_tx = partial(mock_query_tx, m, node_addr)

    # Mock Get Block
    stub_blockdata(
        height,
        "9DDE2673138D3F98313144D6D6167F5FA0D86969CF183C63D453C1A763C833E1",
        "B2951BFC41D220588777428E6CD6F8D4664EAA9044DEC73EDE569EF2D3893DB1",
        "soju-0013",
    )

    # Mock Get Tx
    stub_query_tx(
        18557,
        "4F140DBFA66D4B4B1824FE4CA2DAC77F91DD7EDB86042277F696453C37F67175",
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
        18557,
        "DC9067B9291CF080CADB244B424AD7C2C05D852D49FEE65F172D3E5EFF6971EA",
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
