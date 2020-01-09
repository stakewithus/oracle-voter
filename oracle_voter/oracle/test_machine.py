import asyncio
from asyncio import Future
from oracle_voter.chain.core import LCDNode
from oracle_voter.chain.fixtures_core import stub_lcd_node
from oracle_voter.wallet.fixtures_cli import stub_wallet
from oracle_voter.wallet.cli import CLIWallet
from oracle_voter.config.test_settings import get_settings
from oracle_voter.oracle.fixtures_machine import stub_oracle
from unittest.mock import Mock, patch

from oracle_voter.oracle.machine2 import (
    Oracle,
)
from oracle_voter.feeds.markets import ExchangeErr
from oracle_voter.oracle.fixtures_machine import feed_mocks
test_settings = get_settings()
cli_accounts = (test_settings.get('validator_addr'), test_settings.get('feeder_addr'))

async def main_voting_e2e_3_periods(
    LCDNodeMock,
    CLIWalletMock,
    vote_period,
):
    """LCDNodeMock is a Mocked LCDNode Instance with autospec
    These are the function calls inside machine2.py that uses LCDNode
        - get_tx(tx_hash)
        - get_latest_block()
        - get_oracle_rates()
        - get_oracle_active_denoms()
        - get_oracle_prevotes_validator(denom=denom, validator_addr=self.validator_addr)
        - broadcast_tx_async(json.dumps({ tx: object, mode: "sync" }))
    """

    """CLIWalletMock is a Mocked CLIWallet Instance with autospec
    These are the function calls inside machine2.py that uses wallet
        - sync_wallet
    Properties Accessed (Read-Only)
        - account_num
        - account_addr
    Properties Mutated (Read-Write)
        - account_seq
    """

    """
    ---------------
    | Block 18549 |
    ---------------
    """
    stub_lcd_node(18549, LCDNodeMock, cli_accounts)
    stub_wallet(18549, CLIWalletMock)
    oracle = Oracle(
        vote_period=vote_period,
        lcd_node=LCDNodeMock,
        validator_addr=cli_accounts[0],
        wallet=CLIWalletMock,
    )
    stub_oracle(18549, oracle)
    await oracle.retrieve_height()
    """
    ---------------
    | Block 18550 |
    ---------------
    """
    stub_lcd_node(18550, LCDNodeMock, cli_accounts)
    stub_wallet(18550, CLIWalletMock)
    stub_oracle(18550, oracle)
    await oracle.retrieve_height()
    """
    ---------------
    | Block 18555 |
    ---------------
    """
    stub_lcd_node(18555, LCDNodeMock, cli_accounts)
    stub_wallet(18555, CLIWalletMock)
    stub_oracle(18555, oracle)
    await oracle.retrieve_height()

    """
    ---------------
    | Block 18559 |
    ---------------
    """
    stub_lcd_node(18559, LCDNodeMock, cli_accounts)
    await oracle.retrieve_height()
    

@patch('oracle_voter.oracle.machine2.supported_rates', feed_mocks)
@patch('oracle_voter.chain.core.LCDNode', autospec=True)
@patch('oracle_voter.wallet.cli.CLIWallet', autospec=True)
def a_test_voting_e2e_3_periods(
    CLIWalletMock,
    LCDNodeMock,
):
    # Start Loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_voting_e2e_3_periods(
        LCDNodeMock, # Instance of LCDNode
        CLIWalletMock, # Instance of CLIWallet
        5,  # Vote Period
    ))

def async_raiser(err):
    f = asyncio.Future()
    f.set_exception(err)
    return f

async def handle_coinone_exchange_error(
    CLIWalletMock,
    LCDNodeMock,
    fetch_coinone_krw,
    vote_period,
):
    stub_lcd_node(18549, LCDNodeMock, cli_accounts)
    stub_wallet(18549, CLIWalletMock)
    oracle = Oracle(
        vote_period=vote_period,
        lcd_node=LCDNodeMock,
        validator_addr=cli_accounts[0],
        wallet=CLIWalletMock,
    )
    stub_oracle(18549, oracle)
    print('fetch_coinone_krw', fetch_coinone_krw)
    
    fetch_coinone_krw.side_effect = async_raiser(
        ExchangeErr("Coinone KRW", ""))
    await oracle.retrieve_height()


@patch('oracle_voter.feeds.markets.fetch_coinone_krw', autospec=True)
@patch('oracle_voter.chain.core.LCDNode', autospec=True)
@patch('oracle_voter.wallet.cli.CLIWallet', autospec=True)
def test_handle_coinone_exchange_error(
    CLIWalletMock,
    LCDNodeMock,
    fetch_coinone_krw,
):
    # Start Loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handle_coinone_exchange_error(
        CLIWalletMock,
        LCDNodeMock,
        fetch_coinone_krw,
        5,  # Vote Period
    ))
