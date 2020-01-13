from oracle_voter import _version
import asyncio
import pytest
from unittest.mock import Mock, patch
from oracle_voter.common.util import (
    async_stubber,
    async_raiser,
    not_found
)
from oracle_voter.wallet.cli import CLIWallet
from oracle_voter.chain.mocks.fixture_18549 import account_info, mock_account_info


@patch('subprocess.check_output', autospec=True)
def test_get_addr(mock):
    mock.return_value = bytes("terra1kk2gcmy6d444jpsg3hyf84lxd3dx0naud0236f", "utf-8")
    result = CLIWallet.get_addr("feeder", "")
    assert result == "terra1kk2gcmy6d444jpsg3hyf84lxd3dx0naud0236f"
    

@patch('oracle_voter.chain.core.LCDNode', autospec=True)
def test_sync_state(LCDNodeMock):
    acc_addr = "terra1kk2gcmy6d444jpsg3hyf84lxd3dx0naud0236f"
    LCDNodeMock.get_account.return_value = account_info(acc_addr)
    cli_wallet = CLIWallet("feeder", "", acc_addr, LCDNodeMock)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cli_wallet.sync_state())
    assert str(cli_wallet.account_balance) == "100.000000"
    assert cli_wallet.account_num == "52"
    assert cli_wallet.account_seq == 77


@patch('oracle_voter.chain.core.LCDNode', autospec=True)
def test_sync_state_exception(LCDNodeMock):
    acc_addr = "terra1kk2gcmy6d444jpsg3hyf84lxd3dx0naud0236f"
    LCDNodeMock.get_account.return_value = async_stubber(
        mock_account_info(acc_addr, "public_key", "0", 0, 0))
    cli_wallet = CLIWallet("feeder", "", acc_addr, LCDNodeMock)
    loop = asyncio.get_event_loop()
    with pytest.raises(ValueError):
        loop.run_until_complete(cli_wallet.sync_state())


