"""terra-oracle-voter
Usage:
  main.py start <validator> <wallet> [ --node <lcd_node_addr> \
    --vote-period <vote_period> \
    --password <password> \
    --chain-id <chain_id> \
]
  main.py ( -h | --help )
  main.py ( -v | --version )
Options:
  -h --help    Show this screen.
  -v --version    Show version.
"""

from docopt import docopt
import asyncio

from oracle.machine2 import Oracle
from chain.core import LCDNode
from wallet.cli import CLIWallet
from _version import __version__


async def start_coro(args):
    lcd_node_addr = args["<lcd_node_addr>"]
    validator_addr = args["<validator>"]
    wallet_name = args["<wallet>"]
    wallet_password = args["<password>"]
    vote_period = args["<vote_period>"]
    chain_id = args["<chain_id>"]

    n = LCDNode(addr=lcd_node_addr)
    w = CLIWallet(
        wallet_name,
        wallet_password,
        lcd_node=n,
    )
    # Sync Wallet
    await w.sync_state()

    # Init the Start Machine
    oracle = Oracle(
        vote_period=vote_period,
        lcd_node=n,
        validator_addr=validator_addr,
        wallet=w,
        chain_id=chain_id,
    )
    while True:
        await oracle.retrieve_height()
        await asyncio.sleep(0.50)


def start(args):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_coro(args))


cmds = {
  "start": start,
}


def handle_args(args):
    # Find Cmd
    cmd_key, = [c for c in cmds.keys() if args[c] is True]
    cmds[cmd_key](args)


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    handle_args(arguments)
