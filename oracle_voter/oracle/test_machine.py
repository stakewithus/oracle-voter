import asyncio
from asyncio import Future
from unittest.mock import Mock, patch, MagicMock
from oracle_voter.chain.core import LCDNode
from oracle_voter.chain.fixtures_core import (
    get_latest_block as stub_get_latest_block,
)
from oracle_voter.wallet.fixtures import (
    sync_state as stub_sync_state,
)
from oracle_voter.wallet.cli import CLIWallet
from oracle_voter.config.test_settings import get_settings

from oracle_voter.oracle.machine2 import (
    Oracle,
)

test_settings = get_settings()
async def main_voting_e2e_3_periods(
    http_mock,
    LCDNodeMock,
    CLIWalletMock,
    feed_coinone_url,
    feed_ukfx_url,
    vote_period,
):
    cli_accounts = (test_settings.get('validator_addr'), test_settings.get('feeder_addr'))
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
    blk = 18549
    # get_latest_block
    LCDNodeMock.get_latest_block.return_value = stub_get_latest_block(blk)
    oracle = Oracle(
        vote_period=vote_period,
        lcd_node=LCDNodeMock,
        validator_addr=cli_accounts[0],
        wallet=CLIWalletMock,
    )
    # sync_state
    CLIWalletMock.sync_state.return_value = stub_sync_state(blk, CLIWalletMock)
    await oracle.retrieve_height()
    

@patch('oracle_voter.chain.core.LCDNode', autospec=True)
@patch('oracle_voter.wallet.cli.CLIWallet', autospec=True)
def test_voting_e2e_3_periods(
    CLIWalletMock,
    LCDNodeMock,
    http_mock,
    feed_coinone_url,
    feed_ukfx_url,
):
    # Start Loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_voting_e2e_3_periods(
        http_mock,
        LCDNodeMock, # Instance of LCDNode
        CLIWalletMock, # Instance of CLIWallet
        feed_coinone_url,
        feed_ukfx_url,
        5,  # Vote Period
    ))
