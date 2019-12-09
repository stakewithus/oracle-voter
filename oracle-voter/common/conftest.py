"""

session_mock.side_effect = [
    SessionOk(),
    Session404(),
]


@patch(
@pytest.fixture
def mock_client_session():
    pass
aiohttp.ClientSession = session_mock
"""
