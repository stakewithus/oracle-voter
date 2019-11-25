from feeds.base import Base
from common import client
from decimal import Decimal


class Coinone(Base):

    def __init__(self, api_url):
        super().__init__(api_url)

    def format_trade(self, complete_order):
        px = Decimal(complete_order["price"])
        qty = Decimal(complete_order["qty"])
        side = 1  # Long
        if complete_order["is_ask"] == "1":
            side = 0  # Short
        ts = complete_order["timestamp"]
        return (ts, px, qty, side)

    def postpro_trades(self, http_res):
        result = dict()
        error_code = http_res["errorCode"]
        if error_code != "0":
            return error_code, result
        fetch_ts = http_res["timestamp"]
        # Convert raw trade history into common format
        complete_orders = http_res["completeOrders"]
        trades = [self.format_trade(order) for order in complete_orders]
        return None, {"fetch_ts": fetch_ts, "trades": trades}

    async def get_trades(self, currency):
        get_params = {"currency": currency, "format": "json"}
        target_url = f"{self.api_url}/trades/"
        http_res = await client.http_get(target_url, params=get_params)
        return self.postpro_trades(http_res)
