import asyncio
from asyncio import Future
from unittest.mock import Mock, patch, MagicMock
from oracle_voter.chain.core import LCDNode
from oracle_voter.wallet.cli import CLIWallet
from oracle_voter.config.test_settings import get_settings

from oracle_voter.oracle.machine2 import (
    Oracle,
)

from oracle_voter.chain.mocks.fixture_18549 import mock_height_18549
from oracle_voter.chain.mocks.fixture_18550 import mock_height_18550
from oracle_voter.chain.mocks.fixture_18555 import mock_height_18555
from oracle_voter.chain.mocks.fixture_18559 import mock_height_18559
from oracle_voter.chain.mocks.fixture_terracli import (
    offline_sign_18549,
    offline_sign_18550,
    offline_sign_18555,
)

test_settings = get_settings()
async def main_voting_e2e_3_periods(
    http_mock,
    LCDNodeMock,
    feed_coinone_url,
    feed_ukfx_url,
    vote_period,
):
    cli_accounts = (test_settings.get('validator_addr'), test_settings.get('feeder_addr'))
    lcd_node = LCDNodeMock.return_value
    mock_height_18549(
        http_mock,
        feed_coinone_url,
        feed_ukfx_url,
        cli_accounts,
        lcd_node
    )
    feeder_wallet = CLIWallet(
        test_settings.get('feeder_account'),
        test_settings.get('feeder_pw'),
        cli_accounts[1],
        lcd_node,
    )
    offline_sign_18549(feeder_wallet)
    #Fetch Initial State
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
        feed_coinone_url,
        feed_ukfx_url,
        cli_accounts,
        lcd_node,
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
    offline_sign_18550(feeder_wallet)
    await oracle.retrieve_height()
    #
    # Mock Height 18555
    #
    mock_height_18555(
        http_mock,
        feed_coinone_url,
        feed_ukfx_url,
        cli_accounts,
        lcd_node,
    )
    # Mock the Salts
    salt_mock = Mock()
    salt_mock.side_effect = [
        "3595",
        "39ff",
        "4721",
        "0c26",
    ]
    oracle.get_rate_salt = salt_mock
    offline_sign_18555(feeder_wallet)
    await oracle.retrieve_height()
    #
    # Mock Height 18559
    #
    mock_height_18559(
        http_mock,
        feed_coinone_url,
        feed_ukfx_url,
        cli_accounts,
        lcd_node,
    )
    await oracle.retrieve_height()


@patch('oracle_voter.chain.core.LCDNode', autospec=True)
def test_voting_e2e_3_periods(
    LCDNodeMock,
    http_mock,
    feed_coinone_url,
    feed_ukfx_url,
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
        LCDNodeMock,
        feed_coinone_url,
        feed_ukfx_url,
        5,  # Vote Period
    ))
