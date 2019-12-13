"""
from oracle.fixture_18549 import mock_height_18549
from oracle.fixture_18550 import mock_height_18550


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

    mock_height_18550(
        m,
        node_addr,
        feed_coinone_url,
        feed_ukfx_url,
        cli_accounts,
        feeder_wallet,
    )
"""
