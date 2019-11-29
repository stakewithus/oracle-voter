import asyncio
from oracle.machine2 import main
from oracle.fixtures_machine import voting_e2e_3_periods


def test_voting_e2e_3_periods(
    http_mock,
    node_addr,
    validator_addr,
    feeder_addr,
    wallet_name,
    wallet_password,
):

    # Mock all required endpoints
    voting_e2e_3_periods(http_mock, node_addr, feeder_addr)

    # Start Loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(
        vote_period=5,
        lcd_node_addr=node_addr,
        validator_addr=validator_addr,
        wallet_name=wallet_name,
        wallet_password=wallet_password
    ))
