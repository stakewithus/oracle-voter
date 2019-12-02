import asyncio
from oracle.machine2 import (
    Oracle,
)

from oracle.fixtures_machine import voting_e2e_3_periods


async def main_voting_e2e_3_periods(
    vote_period,
    lcd_node,
    cli_accounts,
    wallet,
):
    # Fetch Initial State
    await wallet.sync_state()

    # Init the Start Machine
    oracle = Oracle(
        vote_period=vote_period,
        lcd_node=lcd_node,
        validator_addr=cli_accounts[0],
        wallet=wallet,
    )
    height_1 = 76777
    # Feed in the first height
    await oracle.new_height(height_1)


def test_voting_e2e_3_periods(
    http_mock,
    node_addr,
    lcd_node,
    cli_accounts,
    feeder_wallet,
):

    # Mock all required endpoints
    voting_e2e_3_periods(http_mock, node_addr, cli_accounts)

    # Start Loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_voting_e2e_3_periods(
        5,
        lcd_node,
        cli_accounts,
        feeder_wallet,
    ))
