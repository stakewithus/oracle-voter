from oracle_voter.base.api import API
from oracle_voter.base.errors import ExchangeError, HttpError
from oracle_voter.base.money import Note


class Coinone:

    base_url = "https://api.coinone.co.kr"

    supported_pairs = [
        "LUNA",
    ]

    def __init__(self, config={}):
        self._api = API(dict(base_url=self.base_url))

    def format_order(self, odr):
        px = Note(odr["price"])
        qty = Note(odr["qty"])
        return px, qty

    def handle_orderbook(self, api_resp):
        exchange_error_code = api_resp.get("errorCode", "-1")

        if exchange_error_code != "0":
            # TODO Log Error
            return None

        ts = api_resp.get("timestamp")
        asks = [self.format_order(odr) for odr in api_resp.get("ask", [])]
        bids = [self.format_order(odr) for odr in api_resp.get("bid", [])]

        return ts, asks, bids

    async def get_orderbook(self, currency):
        if currency not in self.supported_pairs:
            raise ExchangeError(f"Unsupported currency: {currency}")
        try:
            api_resp = await self._api.fetch(
                "orderbook/",
                query=dict(currency=currency, format="json"),
            )
            if api_resp is None:
                return api_resp
            return self.handle_orderbook(api_resp)
        except HttpError:
            return None
