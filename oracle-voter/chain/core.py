from decimal import Decimal
from chain.utils import LexiSortDict
import simplejson as json

EIGHTEEN_PLACES = Decimal(10) ** -18


class Transaction:

    def __init__(
        self,
        chain_id,
        account_number,
        sequence,
        memo="",
    ):
        self.chain_id = chain_id
        self.account_number = str(account_number)
        self.sequence = str(sequence)
        self.memo = memo
        self.fee = {
            "amount": list(),
            "gas": "200000",
        }
        self.msgs = list()
        self.signatures = None

    def append_votemsg(
        self,
        exchange_rate="",
        denom="",
        feeder="",
        validator="",
        salt=None,
    ):
        # Currency Rate is 18 Decimals
        rate = "-1.000000000000000000"
        if isinstance(exchange_rate, Decimal):
            rate = str(exchange_rate.quantize(EIGHTEEN_PLACES))

        msg_salt = None

        if salt is not None:
            msg_salt = salt

        msg = {
            "type": r"oracle\/MsgExchangeRateVote",
            "value": {
                "exchange_rate": rate,
                "salt": msg_salt,
                "denom": denom,
                "feeder": feeder,
                "validator": validator,
            },
        }
        self.msgs.append(msg)

    def export(self, fmt="json"):
        tx = {
            "chain_id": self.chain_id,
            "account_number": self.account_number,
            "sequence": self.sequence,
            "fee": self.fee,
            "msgs": self.msgs,
            "memo": self.memo,
        }
        if self.signatures is not None:
            tx["signatures"] = self.signatures
        return tx

    def sign(self, wallet):
        raw_payload = self.export()
        sign_payload = json.dumps(LexiSortDict(raw_payload))
        print("--sign-payload")
        print(sign_payload)
        print("--sign-payload")
        signature = wallet.sign(sign_payload)
        print(signature)


class FullNode:

    def __init__(
        self,
        addr="http://127.0.0.1:26657",
    ):
        pass


class LCDNode:

    def __init__(
        self,
        addr="http://127.0.0.1:1317",
    ):
        pass
