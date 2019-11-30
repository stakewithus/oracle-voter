import asyncio

from chain.core import Transaction
from wallet.cli import CLIWallet


class State:
    def __init__(self, name): self.name = name
    def __str__(self): return self.name


State.init = State("Init")
State.ready = State("Ready")
State.querying = State("Querying")
State.pre_decision = State("PreDecision")
State.voting = State("Voting")
State.prevoting = State("PreVoting")
State.broadcasting = State("Broadcasting")
State.post_decision = State("PostDecision")


class Input:
    pass


class NewVotingPeriod(Input):

    def __init__(self, height, voting_period):
        self.height = height
        self.voting_period = voting_period


class Condition:

    @staticmethod
    def test(self, input_data):
        assert 0, "Abstract Method test() not implemented"


class Transition:

    @staticmethod
    async def run(oracle_state, input_data):
        assert 0, "Method run() not implemented"


class Oracle:

    def __init__(
        self,
        vote_period=1,
        lcd_node=None,
        validator_addr=None,
        wallet=None,
    ):
        self.vote_period = 1
        self.lcd_node = lcd_node
        self.validator_addr = validator_addr
        self.wallet = wallet
        self.transition_map = {
            (State.init, NewVotingPeriod): (None, State.querying),
        }

    async def next(candidate_input):
        pass


async def main(
    vote_period=1,
    lcd_node_addr="",
    validator_addr="",
    wallet_name="",
    wallet_password="",
):
    lcd_node = LCDNode(lcd_node_addr)
    # TODO Write Test Case to check for following failures
    # - wallet_name is not found in the list of accounts
    wallet = CLIWallet(
        wallet_name,
        wallet_password,
        lcd_node=lcd_node,
    )
    # Attempt to sync state from chain
    try:
        # TODO Write Test Case to check for following failures
        # - feeder account has 0 account_number (not registered)
        # - LCD Node cannot be reached
        # - LCD Node returns non 20x HTTP Error

        await wallet.sync_state()

        oracle = Oracle(
            vote_period=vote_period,
            lcd_node=lcd_node,
            validator_addr=validator_addr,
            wallet=wallet,
        )

    except:
        pass
