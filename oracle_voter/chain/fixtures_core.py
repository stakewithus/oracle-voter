from oracle_voter.chain.mocks.fixture_18549 import mock_height_18549
from oracle_voter.chain.mocks.fixture_18550 import mock_height_18550
from oracle_voter.chain.mocks.fixture_18555 import mock_height_18555
from oracle_voter.chain.mocks.fixture_18559 import mock_height_18559


def stub_lcd_node(height, LCDNodeMock, cli_accounts):
    if height == 18549:
        return mock_height_18549(LCDNodeMock, cli_accounts)
    if height == 18550:
        return mock_height_18550(LCDNodeMock, cli_accounts)
    if height == 18555:
        return mock_height_18555(LCDNodeMock, cli_accounts)
    if height == 18559:
        return mock_height_18559(LCDNodeMock, cli_accounts)
