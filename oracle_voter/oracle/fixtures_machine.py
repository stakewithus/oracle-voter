from unittest.mock import Mock, MagicMock
from decimal import Decimal
from oracle_voter.chain.mocks.fixture_utils import async_stubber

salt_mocks = {
    "18549": [
        "bfaf",
        "41a5",
        "9d6e",
        "28ef",
    ],
    "18550": [
        "ff2e",
        "2d3c",
        "1e47",
        "d534",
    ],
    "18555": [
        "3595",
        "39ff",
        "4721",
        "0c26",
    ]
}

# def stubFeed(value):
#     return async_stubber(Decimal(str(value)));

# feeds = {
#     "18549": [stubFeed(30039.6), stubFeed(225.758), stubFeed(0.0609424), stubFeed(0.0839377)],
#     "18550": [stubFeed(30039.6), stubFeed(225.758), stubFeed(0.0609424), stubFeed(0.0839377)],
#     "18555": [stubFeed(30039.6), stubFeed(225.758), stubFeed(0.0609424), stubFeed(0.0839377)]
# }

def stub_oracle(height, Oracle):
    salt_mock = Mock()
    salt_mock.side_effect = salt_mocks[str(height)]
    Oracle.get_rate_salt = salt_mock
    # feed_mock = MagicMock()
    # feed_mock.side_effect = feeds[str(height)]
    # Oracle.query_feed = feed_mock
    
