from oracle_voter.markets import fixtures_pricing
from decimal import Decimal


def test_calc_microprice_one(calc_microprice):
    result = calc_microprice(fixtures_pricing.get_orderbook_one())
    assert result == Decimal("263.563")
