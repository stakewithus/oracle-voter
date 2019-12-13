from functools import reduce
from decimal import Decimal, getcontext


def sum_volumes(acc, order_row):
    px, qty = order_row
    return acc + qty


def calc_microprice(orderbook, levels=3):
    getcontext().prec = 6  # 6 Significant Figures
    asks_vol = reduce(sum_volumes, orderbook["asks"][0:levels], Decimal("0.0"))
    bids_vol = reduce(sum_volumes, orderbook["bids"][0:levels], Decimal("0.0"))

    ask_px, ask_qty = orderbook["asks"][0]
    bid_px, bid_qty = orderbook["bids"][0]

    microprice = (
        ask_px * asks_vol + bid_px * bids_vol
    ) / (bids_vol + asks_vol)
    return microprice
