import asyncio
from unittest.mock import Mock
from oracle.machine2 import (
    Oracle,
)

# from oracle.fixtures_machine import voting_e2e_3_periods
from oracle.fixture_18549 import mock_height_18549
from oracle.fixture_18550 import mock_height_18550
from oracle.fixture_18555 import mock_height_18555


async def main_voting_e2e_3_periods(
    http_mock,
    node_addr,
    feed_coinone_url,
    feed_ukfx_url,
    cli_accounts,
    feeder_wallet,
    vote_period,
    lcd_node,
):
    mock_height_18549(
        http_mock,
        node_addr,
        feed_coinone_url,
        feed_ukfx_url,
        cli_accounts,
        feeder_wallet,
    )
    # Fetch Initial State
    await feeder_wallet.sync_state()

    # Init the Start Machine
    oracle = Oracle(
        vote_period=vote_period,
        lcd_node=lcd_node,
        validator_addr=cli_accounts[0],
        wallet=feeder_wallet,
    )
    # Mock the Salts
    salt_mock = Mock()
    salt_mock.side_effect = [
        "bfaf",
        "41a5",
        "9d6e",
        "28ef",
    ]
    oracle.get_rate_salt = salt_mock
    # End Mock the Salts
    await oracle.retrieve_height()
    #
    # Mock Height 18550
    #
    mock_height_18550(
        http_mock,
        node_addr,
        feed_coinone_url,
        feed_ukfx_url,
        cli_accounts,
        feeder_wallet,
    )
    # Mock the Salts
    salt_mock = Mock()
    salt_mock.side_effect = [
        "ff2e",
        "2d3c",
        "1e47",
        "d534",
    ]
    oracle.get_rate_salt = salt_mock
    await oracle.retrieve_height()
    #
    # Mock Height 18555
    #
    mock_height_18555(
        http_mock,
        node_addr,
        feed_coinone_url,
        feed_ukfx_url,
        cli_accounts,
        feeder_wallet,
    )
    # Mock the Salts
    salt_mock = Mock()
    salt_mock.side_effect = [
        "ff2e",
        "2d3c",
        "1e47",
        "d534",
    ]
    oracle.get_rate_salt = salt_mock
    await oracle.retrieve_height()


def test_voting_e2e_3_periods(
    http_mock,
    node_addr,
    lcd_node,
    cli_accounts,
    feed_coinone_url,
    feed_ukfx_url,
    feeder_wallet,
):

    # Mock all required endpoints
    """
    voting_e2e_3_periods(
        http_mock,
        node_addr,
        feed_coinone_url,
        feed_ukfx_url,
        cli_accounts,
        feeder_wallet,
    )
    """

    # Start Loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_voting_e2e_3_periods(
        http_mock,
        node_addr,
        feed_coinone_url,
        feed_ukfx_url,
        cli_accounts,
        feeder_wallet,
        5,  # Vote Period
        lcd_node,
    ))
