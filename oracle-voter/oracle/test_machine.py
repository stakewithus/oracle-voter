import asyncio
from oracle.machine2 import (
    Oracle,
    State,
    NewVotingPeriod,
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
        validator_addr=cli_accounts[1],
        wallet=wallet,
    )
    assert oracle.state == State.init

    # Start the Machine
    input_1 = NewVotingPeriod(76777, 15355)
    await oracle.next(input_1)
    assert oracle.state == State.ready


def test_voting_e2e_3_periods(
    http_mock,
    node_addr,
    cli_accounts,
    feeder_wallet,
):

    # Mock all required endpoints
    voting_e2e_3_periods(http_mock, node_addr, cli_accounts)

    # Start Loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_voting_e2e_3_periods(
        5,
        node_addr,
        cli_accounts,
        feeder_wallet,
    ))
