from chain.core import FullNode, LCDNode, Transaction
from wallet.cli import CLIWallet


async def main(
    vote_period=1,
    lcd_node_addr="",
    validator_addr="",
    wallet_name="",
    wallet_password="",
):
    lcd_node = LCDNode(lcd_node_addr)
    feeder_wallet = CLIWallet(
        wallet_name,
        wallet_password,
        lcd_node=lcd_node,
    )
    # Attempt to sync state from chain
    try:
        await feeder_wallet.sync_state()
    except:
        pass
