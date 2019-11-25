from decimal import Decimal


def get_orderbook_one():
    result = {
        "fetch_ts": "1574683544",
        "asks": [
            (Decimal('264.0'), Decimal('3583.053')),
            (Decimal('265.0'), Decimal('378.8709')),
            (Decimal('266.0'), Decimal('601.7191')),
        ],
        "bids": [
            (Decimal('263.0'), Decimal('609.1189')),
            (Decimal('262.0'), Decimal('749.1645')),
            (Decimal('261.0'), Decimal('2179.129')),
        ],
    }
    return result
