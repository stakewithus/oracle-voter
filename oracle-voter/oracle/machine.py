import asyncio
from common import client
from chain.core import LCDNode


class OracleState:
    def __init__(self, name): self.name = name
    def __str__(self): return self.name


OracleState.init = OracleState("Init")
OracleState.inactive = OracleState("Inactive")
OracleState.active = OracleState("Active")


class Input:
    def __init__(self, name):
        self.name = name
        self.value = None

    def __str__(self): return f"[{self.name}] {self.value}]"
    def getValue(self): return self.value
    def setValue(self, val): self.value = val


Input.vote = Input("Vote")



class Oracle:
    # Initial State
    state = OracleState.init
    last_block_height = 0
    last_vote_period = 0
    # TODO Get a list of actives instead of hardcoding
    currency = "ukrw"

    def __init__(
        self,
        vote_period=1,
        lcd_node=LCDNode(""),
        validator_addr="",
    ):
        self.lcd_node = lcd_node
        self.vote_period = vote_period
        self.validator_addr = validator_addr

        self.vote_queue = list()

    def height_to_vp(self, height):
        #
        vote_left = height % self.vote_period
        vote_height = height
        if vote_left != 0:
            vote_height = height - vote_left
        vote_period = vote_height / self.vote_period

    async def apply_action(self, oracle_input):
        if isinstance(oracle_input, Input):
            current_height, vote_period = Input.vote.getValue()
            self.last_block_height = current_height
            self.last_vote_period = vote_period
            await self.action_vote()

    async def get_prevotes(self):
        res = await self.lcd_node.get_oracle_prevotes_validator(
            denom=self.currency,
            validator_addr=self.validator_addr
        )
        return res

    async def get_votes(self):
        res = await self.lcd_node.get_oracle_votes_validator(
            denom=self.currency,
            validator_addr=self.validator_addr
        )
        return res

    async def action_vote(self):
        # Get Current Pre-Votes
        # TODO Get pre-votes for multiple currencies
        [prevotes_raw, votes_raw] = await asyncio.gather(
            self.get_prevotes(),
            self.get_votes(),
        )
        # If We Have PreVotes, and they belong
        # To last_vote_period - 1
        # We should vote for them now
        prevotes = prevotes_raw["result"]
        if len(prevotes) > 0:
            # Take the first prevote
            eval_prevote = prevotes[0]
            submitted_vote_period = self.height_to_vp(eval_prevote["submit_block"])
            submitted_hash = eval_prevote["hash"]
            # If the Pre Vote is in the same vote period, do not Vote
            if submitted_vote_period == (self.last_vote_period - 1):
                self.vote_queue.append(submitted_hash) 
        
        print(prevotes_raw)
        print(votes_raw)

    @staticmethod
    async def update_chain_state(oracle):
        if oracle.state == OracleState.active:
            return None
        raw_block_info = await oracle.lcd_node.get_latest_block()
        block_meta = raw_block_info["block_meta"]
        current_height = int(block_meta["header"]["height"])
        vote_left = current_height % oracle.vote_period
        vote_height = current_height
        if vote_left != 0:
            vote_height = current_height - vote_left
        vote_period = vote_height / oracle.vote_period
        print(f"Current BH/VP: {current_height} / {vote_period}")
        """
        When Oracle is in Init State, height=0, vote_period=0
        - Trigger Vote to see if we can vote in the current vote_period
        """
        new_action = None
        if oracle.state == OracleState.init:
            print("In Init State")
            new_action = Input.vote
            payload = (current_height, vote_period)
            new_action.setValue(payload)
        return new_action


async def main(
    vote_period=1,
    lcd_node_addr="",
    validator_addr="",
):
    lcd_node = LCDNode(
        addr=lcd_node_addr,
    )

    oracle = Oracle(
        vote_period=vote_period,
        lcd_node=lcd_node,
        validator_addr=validator_addr,
    )

    while True:
        new_action = await Oracle.update_chain_state(oracle)
        if new_action is not None:
            await oracle.apply_action(new_action)
        await asyncio.sleep(1)
