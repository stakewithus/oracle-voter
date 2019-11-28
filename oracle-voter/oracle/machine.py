import asyncio
from decimal import Decimal, getcontext, Context
from secrets import token_hex
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import simplejson as json

from feeds import coinone
from markets import pricing
from chain.core import FullNode, LCDNode, Transaction
from wallet.cli import CLIWallet

getcontext().prec = 40
EIGHTEEN_PLACES = Decimal("10.0") ** -18


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

exchange_coinone = coinone.Coinone("https://api.coinone.co.kr")


class Oracle:
    # Initial State
    state = OracleState.init
    last_block_height = 0
    last_vote_period = 0
    # TODO Get a list of actives instead of hardcoding
    currency = "ukrw"
    # TODO Support Multiple Rates
    last_known_rate = Decimal("0")
    # TODO Remove Hardcode
    chain_id = "soju-0012"

    prevotes = dict()

    def __init__(
        self,
        vote_period=1,
        lcd_node=LCDNode(""),
        full_node=FullNode(""),
        validator_addr="",
        feeder_wallet=None
    ):
        self.lcd_node = lcd_node
        self.full_node = full_node
        self.vote_period = vote_period
        self.validator_addr = validator_addr
        self.feeder_wallet = feeder_wallet

        self.vote_queue = list()

    def height_to_vp(self, raw_height):
        height = int(raw_height)
        vote_left = height % self.vote_period
        vote_height = height
        if vote_left != 0:
            vote_height = height - vote_left
        vote_period = vote_height / self.vote_period
        return vote_period

    async def apply_action(self, oracle_input):
        if isinstance(oracle_input, Input):
            current_height, vote_period = Input.vote.getValue()
            self.last_block_height = current_height
            self.last_vote_period = vote_period
            await self.action_vote()
            self.state = OracleState.active

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

    async def get_rates(self):
        res = await self.lcd_node.get_oracle_rates()
        return res

    async def update_wallet(self):
        await self.feeder_wallet.update_state()
        return None

    async def action_vote(self):
        print("----- Action -----")
        # Get Current Pre-Votes
        # TODO Get pre-votes for multiple currencies
        [prevotes_raw, votes_raw, rates_raw, _feeder_wallet] = await asyncio.gather(
            self.get_prevotes(),
            self.get_votes(),
            self.get_rates(),
            self.update_wallet(),
        )
        print(prevotes_raw)
        print(votes_raw)
        print(f"""Terra Luna Rate: {rates_raw["result"][0]}""")
        self.last_known_rate = Decimal(rates_raw["result"][0]["amount"])
        # If We Have PreVotes, and they belong
        # To last_vote_period - 1
        # We should vote for them now
        prevotes = prevotes_raw["result"]
        if len(prevotes) > 0:
            # Take the first prevote
            eval_prevote = prevotes[0]
            submitted_vote_period = self.height_to_vp(eval_prevote["submit_block"])
            submitted_hash = eval_prevote["hash"]
            print(f"[PreVote] VotePeriod: {submitted_vote_period} Hash: {submitted_hash}")
            # If the Pre Vote is in the same vote period, do not Vote
            if submitted_vote_period == (self.last_vote_period - 1):
                self.vote_queue.append(submitted_hash)
                print(f"Need to Vote on {submitted_hash}")
        # If We Have Voted for the Hash, Remove From Vote Queue
        votes = votes_raw["result"]
        if len(votes) > 0:
            # Take the first vote
            eval_vote = votes[0]
            query_height = votes_raw["height"]
            vote_vp = self.height_to_vp(query_height)
            print(f"""[Vote] VotePeriod: {vote_vp} Denom: {eval_vote["denom"]} Px: {eval_vote["exchange_rate"]}""")
        # Make Transaction For This Vote Period
        # TODO Load Chain ID from the LCD
        # Do PreVote for This Period
        # Get MicroPrice
        # TODO Remove Hardcode
        target_currency = "LUNA"
        err, orderbook = await exchange_coinone.get_orderbook(target_currency)
        microprice = pricing.calc_microprice(orderbook)
        real_microprice = microprice.quantize(EIGHTEEN_PLACES, context=Context(prec=40))
        print(f"Our Microprice: {real_microprice}")
        # Now Sign and Broadcast Votes
        txb = Transaction(
            self.chain_id, 
            self.feeder_wallet.account_num,
            self.feeder_wallet.account_seq,
        )
        
        # For Votes in VoteQueue, Try to Find the Hash In Prevotes
        broadcast_votes = len(self.vote_queue) > 0
    
        if broadcast_votes is True:
            # Pause abit
            await asyncio.sleep(0.500)
            #
            while len(self.vote_queue) > 0:
                prevote_hash = self.vote_queue.pop()
                if prevote_hash in self.prevotes:
                    vote_data = self.prevotes.pop(prevote_hash, None)
                    txb.append_votemsg(
                        exchange_rate=vote_data["px"],
                        denom=vote_data["denom"],
                        feeder=vote_data["feeder"],
                        validator=vote_data["validator"],
                        salt=vote_data["salt"]
                    )

            # Preview the Tx
            print("----- PreviewPreparedTx -----") 
            preview_tx = txb.build_incomplete()
            print(json.dumps(preview_tx, indent=2, sort_keys=True))
            if len(preview_tx["msgs"]) > 0:
                pass
                # Sign the Tx
                signed_tx = txb.sign(self.feeder_wallet)
                print("----- PreviewSignedTx -----") 
                print(json.dumps(signed_tx, indent=2, sort_keys=True))
                print("----- Action -----")
                """
                Sometimes the account does not update...
                """
                # Bump the sequence
                self.feeder_wallet.account_seq += 1
                # TODO Broadcast the TX
                broadcast_vote_res = await self.full_node.broadcast_tx_async(json.dumps({
                    "tx": signed_tx["value"],
                    "mode": "sync",
                }))
                print(broadcast_vote_res)

        # Submit PreVotes Last, Followed by Votes
        txb = Transaction(
            self.chain_id, 
            self.feeder_wallet.account_num,
            self.feeder_wallet.account_seq,
        )
        # 1. Make the Random Salt
        """ Salt Length is Between 1 - 4 """
        rate_salt = token_hex(2)
        # 2. Make the Payload
        hash_payload = f"{rate_salt}:{str(real_microprice)}:{self.currency}:{self.validator_addr}"
        # 3. SHA256 Payload
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(hash_payload, "utf-8"))
        hashed = digest.finalize().hex()[0:40]
        txb.append_prevotemsg(
            hashed=hashed,
            denom=self.currency,
            feeder=self.feeder_wallet.account_addr,
            validator=self.validator_addr
        )
        # Save PreVote to PreVote Dict
        self.prevotes[hashed] = {
            "px": real_microprice,
            "denom": self.currency,
            "feeder": self.feeder_wallet.account_addr,
            "validator": self.validator_addr,
            "salt": rate_salt,
        }

        # Preview the Tx
        print("----- PreviewPreparedTx -----") 
        print(json.dumps(txb.build_incomplete(), indent=2, sort_keys=True))
        # Sign the Tx
        signed_tx = txb.sign(self.feeder_wallet)
        print("----- PreviewSignedTx -----") 
        print(json.dumps(signed_tx, indent=2, sort_keys=True))
        print("----- Action -----")
        """
        Sometimes the account does not update...
        """
        # Bump the sequence
        self.feeder_wallet.account_seq += 1
        # TODO Broadcast the TX
        broadcast_prevote_res = await self.full_node.broadcast_tx_async(json.dumps({
            "tx": signed_tx["value"],
            "mode": "sync",
        }))
        print(broadcast_prevote_res)

        """ Some Errors 
{'jsonrpc': '2.0', 'id': '', 'error': {'code': -32602, 'message': 'Invalid params', 'data': 'error converting http params to arguments: json: cannot unmarshal object into Go value of type types.Tx'}}

        {'height': '0', 'txhash': '218C96406BBC8DA59AB2447D071C3A59BEEA1F770D9FF9A76E521B31CEB12BBC', 'code': 4, 'raw_log': '{"codespace":"sdk","code":4,"message":"signature verification failed; verify correct account sequence and chain-id"}'}

        {'height': '0', 'txhash': 'C29D654165A98E2FC5299CFFF0C53B9CD235A3843C9130F587CFEE73C3BED62D', 'code': 10, 'raw_log': '{"codespace":"oracle","code":10,"message":"Salt legnth should be 1~4, but given 16"}'}
        """

        """ Success Messages

{'height': '0', 'txhash': 'B4AE35F0AC201B0D1BCCE657DD20F2CF75EAD962668A51B7E308784C9BE7AE0B', 'raw_log': '[{"msg_index":0,"success":true,"log":"","events":[{"type":"message","attributes":[{"key":"action","value":"exchangerateprevote"}]}]}]', 'logs': [{'msg_index': 0, 'success': True, 'log': '', 'events': [{'type': 'message', 'attributes': [{'key': 'action', 'value': 'exchangerateprevote'}]}]}]}

{'height': '0', 'txhash': '25C5797A853CDD9B7FF06715A32285E38FF77D886B424D6211939171E1F06229', 'raw_log': '[{"msg_index":0,"success":true,"log":"","events":[{"type":"message","attributes":[{"key":"action","value":"exchangerateprevote"}]}]},{"msg_index":1,"success":true,"log":"","events":[{"type":"message","attributes":[{"key":"action","value":"exchangeratevote"}]}]}]', 'logs': [{'msg_index': 0, 'success': True, 'log': '', 'events': [{'type': 'message', 'attributes': [{'key': 'action', 'value': 'exchangerateprevote'}]}]}, {'msg_index': 1, 'success': True, 'log': '', 'events': [{'type': 'message', 'attributes': [{'key': 'action', 'value': 'exchangeratevote'}]}]}]}
        """
        print("----- Action -----")

    @staticmethod
    async def update_chain_state(oracle):
        if oracle.state == OracleState.inactive:
            return None
        raw_block_info = await oracle.lcd_node.get_latest_block()
        block_meta = raw_block_info["block_meta"]
        current_height = int(block_meta["header"]["height"])
        vote_left = current_height % oracle.vote_period
        vote_height = current_height
        if vote_left != 0:
            vote_height = current_height - vote_left
        vote_period = vote_height / oracle.vote_period
        """
        When Oracle is in Init State, height=0, vote_period=0
        - Trigger Vote to see if we can vote in the current vote_period
        """
        height_adjustment = oracle.last_vote_period + oracle.vote_period + 1
        new_action = None
        if oracle.state == OracleState.init:
            new_action = Input.vote
            payload = (current_height, vote_period)
            print(f"Current BH/VP: {current_height} / {vote_period}")
            new_action.setValue(payload)
        elif (oracle.last_vote_period < vote_period and
                current_height > height_adjustment):
            new_action = Input.vote
            payload = (current_height, vote_period)
            print(f"Current BH/VP: {current_height} / {vote_period}")
            new_action.setValue(payload)
        else:
            pass
        return new_action


async def main(
    vote_period=1,
    lcd_node_addr="",
    full_node_addr="",
    validator_addr="",
    wallet_name="",
    wallet_password="",
):
    lcd_node = LCDNode(
        addr=lcd_node_addr,
    )

    full_node = FullNode(
        addr=full_node_addr,
    )    

    feeder_wallet = CLIWallet(
        wallet_name,
        wallet_password,
        lcd_node=lcd_node,
    )
    await feeder_wallet.update_state()

    oracle = Oracle(
        vote_period=vote_period,
        lcd_node=lcd_node,
        full_node=full_node,
        validator_addr=validator_addr,
        feeder_wallet=feeder_wallet,
    )

    while True:
        new_action = await Oracle.update_chain_state(oracle)
        if new_action is not None:
            await oracle.apply_action(new_action)
        await asyncio.sleep(1)
