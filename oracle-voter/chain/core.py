from decimal import Decimal

EIGHTEEN_PLACES = Decimal(10) ** -18


class Transaction:

    def __init__(
        self,
        chain_id,
        account_number,
        memo="",
    ):
        self.chain_id = chain_id
        self.account_number = str(account_number)
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
        demon="",
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
            "type": "oracle/MsgExchangeRateVote",
            "value": {
                "exchange_rate": rate,
                "salt": msg_salt,
                "demon": demon,
                "feeder": feeder,
                "validator": validator,
            },
        }
        self.msgs.append(msg)

    def export(self, fmt="json"):
        tx = {
            "chain_id": self.chain_id,
            "account_number": self.account_number,
            "fee": self.fee,
            "msgs": self.msgs,
            "memo": self.memo,
        }
        if self.signatures is not None:
            tx["signatures"] = self.signatures
        return tx

    def sign(self, wallet):
        pass


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
