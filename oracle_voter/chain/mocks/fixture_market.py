#pylint: disable-msg=too-many-arguments
from unittest.mock import MagicMock

from oracle_voter.chain.mocks.fixture_utils import (
    mock_feed_coinone_orderbook,
    mock_feed_ukfx_px
)

def mock_init(
    http_mock,
    feed_coinone_url="",
    feed_ukfx_url="",
):
    mock_feed_ukfx_px(http_mock, feed_ukfx_url, "mnt", [[1575541429000, 2.2575782374764977]])
    mock_feed_ukfx_px(http_mock, feed_ukfx_url, "usd", [[1575541429000, 0.0008393768466290626]])
    mock_feed_ukfx_px(http_mock, feed_ukfx_url, "xdr", [[1575541429000, 0.0006094236838571045]])
    mock_feed_coinone_orderbook(http_mock, feed_coinone_url, "LUNA", [
        {"price": "301.0", "qty": "1902.6306"},
        {"price": "302.0", "qty": "1861.4027"},
        {"price": "303.0", "qty": "200.0"},
    ], [
        {"price": "299.0", "qty": "641.5213"},
        {"price": "298.0", "qty": "1071.129"},
        {"price": "297.0", "qty": "2.0"},
    ])
    
