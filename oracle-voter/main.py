import asyncio
from oracle.machine import main

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(
        vote_period=5,
        lcd_node_addr="http://18.197.124.43:1321",
        # full_node_addr="http://18.197.124.43:56657",
        full_node_addr="http://18.197.124.43:1321",
        # Thanks Dokia
        validator_addr="terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",
        wallet_name="oracle",
        wallet_password="12345678",
    ))
