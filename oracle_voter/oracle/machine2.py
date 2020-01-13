# import asyncio

# from chain.core import Transaction
# from wallet.cli import CLIWallet
from functools import partial, reduce
from secrets import token_hex
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from aiohttp.client_exceptions import ClientConnectionError
from decimal import Decimal, Context
import asyncio
import simplejson as json
from collections import deque, OrderedDict

from oracle_voter.oracle.utils import get_vote_period
from oracle_voter.feeds.markets import supported_rates, WEI_VALUE, ABSTAIN_VOTE_PX, ExchangeErr
from oracle_voter.chain.core import Transaction
from oracle_voter.common.client import HttpError

denom_supported_rates = [
    market_info["denom"] for market_info in supported_rates
]


class Oracle:

    def __init__(
        self,
        vote_period=1,
        lcd_node=None,
        validator_addr=None,
        wallet=None,
        chain_id="soju-0012",
        gas_fee="1000",
        gas_denom="uluna",
    ):
        self.vote_period = vote_period
        self.lcd_node = lcd_node
        # TODO Remove hardcode for chain_id
        self.chain_id = chain_id
        self.validator_addr = validator_addr
        self.wallet = wallet
        self.gas_fee = gas_fee
        self.gas_denom = gas_denom

        self.period_getter = partial(get_vote_period, self.vote_period)

        self.current_vote_period = 0
        self.current_height = 0
        self.current_rates = None

        self.prior_prevotes = dict()

        self.q_vote_tx_hash = deque()
        self.q_prevote_tx_hash = deque()

        self.vote_msg_builder = None
        self.prevote_msg_builder = None

        self.hist_votes = OrderedDict()
        self.hist_prevotes = OrderedDict()

        self.rate_luna_ukrw = Decimal("-1.00")
        # Denom to Hash
        self.hash_map = dict()
        self.hist_hash_map = dict()

    """
    External Calls
    """

    """
    We should have predictable error returns or default value returns
    if anoy of the below external call throws
    """
    async def retrieve_tx(self, tx_hash):
        raw_res = await self.lcd_node.get_tx(tx_hash)
        return raw_res

    async def retrieve_height(self):
        raw_res = await self.lcd_node.get_latest_block()
        if raw_res is None:
            return
        block_meta = raw_res["block_meta"]
        current_height = int(block_meta["header"]["height"])
        if current_height > self.current_height:
            self.current_height = current_height
            await self.new_height(int(current_height))

    async def retrieve_chain_rates(self):
        try:
            raw_res = await self.lcd_node.get_oracle_rates()
            rates = raw_res["result"]
            return rates
        except HttpError:
            return None

    async def retrieve_chain_active_denoms(self):
        try:
            raw_res = await self.lcd_node.get_oracle_active_denoms()
            actives = raw_res["result"]
            return actives
        except HttpError:
            return list()

    async def retrieve_prevotes(self, denom):
        try:
            raw_res = await self.lcd_node.get_oracle_prevotes_validator(
                denom=denom,
                validator_addr=self.validator_addr,
            )
            prevotes = raw_res["result"]
            return prevotes
        except HttpError:
            return list()

    async def sync_wallet(self):
        await self.wallet.sync_state()

    async def query_feed(self, market_info):
        try:
            feed_px = await market_info["feed"]()
            feed_weight = market_info["weight"]
            return (feed_px * Decimal(feed_weight))
        except ExchangeErr as err:
            print(err)
            print(err.exchange_err)
            return None
        except HttpError:
            return None

    async def get_denom_px(self, markets):
        task_feed = [
            self.query_feed(market_info) for market_info in markets
        ]
        feed_weights = [market_info["weight"] for market_info in markets]
        # Sum of all the weights assigned in the feed's markets
        total_weight = reduce(
            lambda acc, x: acc + x,
            feed_weights,
            Decimal("0.0"),
        )
        market_pxs = await asyncio.gather(*task_feed)
        # If any market_pxs return None
        # We abstain
        failed_market_px = [mpx for mpx in market_pxs if mpx is None]
        if len(failed_market_px) > 0:
            return ABSTAIN_VOTE_PX
        # Get the mean price of denom
        market_px = reduce(
            lambda acc, px: acc + (px / total_weight),
            market_pxs,
            Decimal("0.0"),
        )
        return market_px

    """
    Internal Logic
    """

    async def append_vote_msg(self, denom):
        prevotes = await self.retrieve_prevotes(denom)
        print("---- PreVotes Seen ----")
        print(json.dumps(prevotes, indent=2))
        print("---- End PreVotes Seen ----")
        if len(prevotes) > 0:
            prevote_data = prevotes[0]
            # Attempt to get the prevote hash from current hashmap
            prevote_cached = self.prior_prevotes.get(
                prevote_data["hash"],
                None,
            )
            # If prevote_cached is None
            # We do not have information on this pre-vote
            # Hence we cannot vote
            if prevote_cached is not None:
                prevote_vp = prevote_cached["vp"]
                print(f"PreVote VP: {prevote_vp} Current VP: {self.current_vote_period}")
                # Get Previous Hashed
                hash_info = self.hash_map.get(denom, None)
                # Do not reveal vote if prior prevote voting period
                # Is the same as the current voting period
                if hash_info is not None and \
                        self.current_vote_period > prevote_vp:
                    rate_salt, hashed = self.hash_map.get(denom)

                    self.vote_msg_builder.append_votemsg(
                        exchange_rate=prevote_cached["px"],
                        denom=denom,
                        feeder=self.wallet.account_addr,
                        validator=self.validator_addr,
                        salt=prevote_cached["salt"],
                    )

    def get_rate_salt(self):
        return token_hex(2)

    def get_prevote_hash(self, denom, px, rate_salt=None):
        if rate_salt is None:
            # 1. Get Salt
            rate_salt = self.get_rate_salt()
        # 2. Make the Payload
        hash_payload = f"{rate_salt}:{str(px)}:{denom}:{self.validator_addr}"
        # 3. SHA256 Payload
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(hash_payload, "utf-8"))
        hashed = digest.finalize().hex()[0:40]
        return rate_salt, hashed

    async def append_prevote_msg(self, denom):
        chain_rate = ABSTAIN_VOTE_PX
        if self.current_rates is not None:
            chain_rates = [
                rate_row["amount"] for rate_row in self.current_rates if
                rate_row["denom"] == denom
            ]
            # On Chain Last Exchange Rate
            chain_rate = Decimal(chain_rates[0])
        # Get Rate Markets
        denom_rate_info = [
            rate_info for rate_info in supported_rates if
            rate_info["denom"] == denom
        ]

        if len(denom_rate_info) > 0:
            raw_markets = denom_rate_info[0]["markets"]

            raw_px = await self.get_denom_px(raw_markets)
            sug_market_px = raw_px.quantize(
                WEI_VALUE,
                context=Context(prec=40),
            )
            #
            # TODO Check that our market_px is not too far away from chain px
            #
            if denom_rate_info[0]["pair_type"] == "native":
                market_px = sug_market_px
            elif raw_px == Decimal("-1.00"):
                market_px = Decimal("-1.00").quantize(
                    WEI_VALUE,
                    context=Context(prec=40),
                )
            else:
                market_px = \
                    Decimal(sug_market_px * self.rate_luna_krw).quantize(
                        WEI_VALUE,
                        context=Context(prec=40),
                    )
            # If we are unable to get the latest exchange rates, abstain vote
            if self.current_rates is not None:
                if chain_rate == ABSTAIN_VOTE_PX:
                    market_px = ABSTAIN_VOTE_PX
                else:
                    # Check that market_px is not more than x percent
                    # From last onchain price
                    px_pct_diff = Decimal(1 - (market_px / chain_rate)).copy_abs()
                    if (px_pct_diff > Decimal("0.02")):
                        market_px = ABSTAIN_VOTE_PX

            if denom == "ukrw":
                self.rate_luna_krw = market_px

            rate_salt, hashed = self.get_prevote_hash(
                denom,
                market_px,
            )

            self.hash_map[denom] = (rate_salt, hashed)

            if self.hist_hash_map.get(denom, None) is None:
                self.hist_hash_map[denom] = dict()

            # self.hist_hash_map[denom][rate_salt] = hashed
            self.hist_hash_map[denom][hashed] = rate_salt

            self.prior_prevotes[hashed] = {
                "px": market_px,
                "salt": rate_salt,
                "vp": int(self.current_vote_period)
            }
            self.prevote_msg_builder.append_prevotemsg(
                hashed=hashed,
                denom=denom,
                feeder=self.wallet.account_addr,
                validator=self.validator_addr,
            )

    async def sign_and_broadcast_votes(self):
        if len(self.vote_msg_builder.msgs) > 0:
            #
            signed_tx = self.vote_msg_builder.sign(self.wallet)
            try:
                broadcast_vote_res = await self.lcd_node.broadcast_tx_async(
                    json.dumps({
                        "tx": signed_tx["value"],
                        "mode": "sync",
                    })
                )
                # TODO Validate that the Vote Has Passed sync
                # self.last_vote_tx_hash = broadcast_vote_res["txhash"]
                query_height = self.current_height + 4
                vote_data = query_height, broadcast_vote_res["txhash"]
                self.q_vote_tx_hash.append(vote_data)
                self.hist_votes[broadcast_vote_res["txhash"]] = {
                    "msgs": signed_tx["value"]["msg"],
                    "sent_height": self.current_height,
                }

                self.wallet.account_seq += 1
            except (HttpError, ClientConnectionError) as err:
                print("Client Connection Issues")
                print(err)
                self.wallet.account_seq += 1

    async def sign_and_broadcast_prevotes(self):
        if len(self.prevote_msg_builder.msgs) > 0:
            #
            try:
                signed_tx = self.prevote_msg_builder.sign(self.wallet)
                broadcast_prevote_res = await self.lcd_node.broadcast_tx_async(
                    json.dumps({
                        "tx": signed_tx["value"],
                        "mode": "sync",
                    })
                )
                # TODO Validate that the PreVote Has Passed sync
                # self.last_prevote_tx_hash = broadcast_prevote_res["txhash"]
                query_height = self.current_height + 1
                prevote_data = query_height, broadcast_prevote_res["txhash"]
                self.q_prevote_tx_hash.append(prevote_data)
                self.hist_prevotes[broadcast_prevote_res["txhash"]] = {
                    "msgs": signed_tx["value"]["msg"],
                    "sent_height": self.current_height,
                }

                self.wallet.account_seq += 1
            except (HttpError, ClientConnectionError) as err:
                print("Client Connection Issues")
                print(err)
                self.wallet.account_seq += 1

    def print_tx_hist(self, tx_hist):
        idx = 1
        for tx_hash, tx_body in tx_hist.items():
            print(f"{idx}. [{tx_hash}]")
            print("-- Msgs")
            for msg in tx_body["msgs"]:
                msg_type = msg["type"]
                msg_val = msg["value"]
                if msg_type == "oracle/MsgExchangeRateVote":

                    print(f"""-- Px {msg_val["exchange_rate"]} Salt: {msg_val["salt"]} \
Denom: {msg_val["denom"]} """)
                else:
                    denom = msg_val["denom"]
                    salt = self.hist_hash_map[denom][msg_val["hash"]]

                    print(f"""-- Hash {msg_val["hash"]} Denom: \
{msg_val["denom"]} Salt: {salt}""")
            if tx_body.get("result", None) is not None:
                tx_height = tx_body["height"]
                success = tx_body.get("result")
                print(f"-- Result: {success} Height: {tx_height}")
                if success is not True:
                    print("-- Failed Logs")
                    for failed_log in tx_body.get("failed_logs"):
                        print(failed_log)
            idx += 1

    async def query_tx(self, height, tx_info):
        tx_type, tx_hash = tx_info
        try:
            raw_res = await self.retrieve_tx(tx_hash)
            raw_height = raw_res["height"]
            raw_logs = raw_res["logs"]
            success = True
            failed_logs = [
                (log_row["msg_index"], log_row["log"])
                for log_row in raw_logs if log_row["success"] is not True
            ]

            if len(failed_logs) > 0:
                success = False

            if tx_type == "vote":
                # Check that all messages passed
                self.hist_votes[tx_hash]["result"] = success
                self.hist_votes[tx_hash]["height"] = raw_height
                if success is not True:
                    self.hist_votes[tx_hash]["failed_logs"] = failed_logs
            else:
                self.hist_prevotes[tx_hash]["result"] = success
                self.hist_prevotes[tx_hash]["height"] = raw_height
                if success is not True:
                    self.hist_prevotes[tx_hash]["failed_logs"] = failed_logs
        except HttpError:
            new_check_height = height + 1
            if tx_type == "vote":
                self.q_vote_tx_hash.appendleft((new_check_height, tx_hash))
            else:
                self.q_prevote_tx_hash.appendleft((new_check_height, tx_hash))

    async def check_txs(self, height):
        tx_hashes = list()
        if len(self.q_vote_tx_hash) > 0:
            leftover_hash = deque()
            while(len(self.q_vote_tx_hash) > 0):
                check_height, vote_tx_hash = self.q_vote_tx_hash.popleft()
                if height >= check_height:
                    tx_hashes.append(('vote', vote_tx_hash))
                else:
                    leftover_hash.appendleft((check_height, vote_tx_hash))
            self.q_vote_tx_hash = leftover_hash

        if len(self.q_prevote_tx_hash) > 0:
            leftover_hash = deque()
            while(len(self.q_prevote_tx_hash) > 0):
                check_height, prevote_tx_hash = self.q_prevote_tx_hash.popleft()
                if height >= check_height:
                    tx_hashes.append(('prevote', prevote_tx_hash))
                else:
                    leftover_hash.appendleft(
                        (check_height, prevote_tx_hash)
                    )
            self.q_prevote_tx_hash = leftover_hash

        tx_querier = partial(self.query_tx, height)
        tx_queries = [tx_querier(tx_info) for tx_info in tx_hashes]

        await asyncio.gather(*tx_queries)
        print(f"----------({height})---------")
        await self.sync_wallet(),
        print(f"----------Votes ---------")
        self.print_tx_hist(self.hist_votes)
        print(f"\n----------PreVotes ---------")
        self.print_tx_hist(self.hist_prevotes)
        print(f"----------({height})---------\n\n")

        # Do some cleanup, show only most recent 3

        if len(self.hist_votes) > 3:
            head = list(self.hist_votes.keys())[0]
            self.hist_votes.pop(head, None)

        if len(self.hist_prevotes) > 3:
            head = list(self.hist_prevotes.keys())[0]
            self.hist_prevotes.pop(head, None)

    async def new_height(self, height):
        vote_period = self.period_getter(height)
        # Check for tx success / fail
        await self.check_txs(height)

        # Vote Period Increased
        if vote_period > self.current_vote_period:
            self.current_vote_period = vote_period
            await self.new_vote_period()

    async def new_vote_period(self):
        # Get Actives
        # Get Rates for All Markets on Chain
        # Update Wallet
        active_rates, current_rates = await asyncio.gather(
            self.retrieve_chain_active_denoms(),
            self.retrieve_chain_rates(),
        )
        if len(active_rates) == 0:
            print("--WARNING-- Terra Chain has no active rates--")
            active_rates = ["ukrw", "uusd", "usdr", "umnt"]
        if current_rates is None:
            print("--WARNING-- Terra Chain has no current rates--")
            self.current_rates = None
        else:
            self.current_rates = current_rates
        # Filter and work on those we have implemented rates for
        calc_rates = [
            denom for denom in active_rates
            if denom_supported_rates.count(denom) > 0
        ]
        # For each support rate

        # 1. Get PreVotes
        # 2a. If PreVotes is not empty, submit Vote
        # 2b  Append VoteMsg to VoteTx
        # 2c. If VoteMsgs length > 0, broadcast VoteTx
        self.vote_msg_builder = Transaction(
            self.chain_id,
            self.wallet.account_num,
            self.wallet.account_seq,
            gas_denom=self.gas_denom,
            gas_fee=self.gas_fee,
        )

        append_vote_tasks = [
            self.append_vote_msg(denom) for denom in calc_rates
        ]
        await asyncio.gather(*append_vote_tasks)
        await self.sign_and_broadcast_votes()

        await asyncio.sleep(0.300)

        # 3a. Get Rate From Chain
        # 3b. Get Rates from various markets
        # 3c. Append PreVoteMsg to VoteTx
        # 3d. If PreVoteMsgs length > 0, broadcast PreVoteTx
        calc_rates = [
            denom for denom in active_rates
            if (denom_supported_rates.count(denom) > 0 and denom != "ukrw")
        ]
        self.prevote_msg_builder = Transaction(
            self.chain_id,
            self.wallet.account_num,
            self.wallet.account_seq,
            gas_denom=self.gas_denom,
            gas_fee=self.gas_fee,
        )
        # Filter Out the base pair luna/ukrw
        # Get Luna UKRW First
        await self.append_prevote_msg("ukrw")

        append_prevote_tasks = [
            self.append_prevote_msg(denom) for denom in calc_rates
        ]
        await asyncio.gather(*append_prevote_tasks)
        await self.sign_and_broadcast_prevotes()
