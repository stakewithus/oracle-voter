import pytest
import asyncio
from unittest.mock import patch
from oracle_voter.common.fixtures_client import (
    SessionOk,
    Session404,
    SessionExceptClientConnection,
    SessionExceptServerTimeout,
    SessionExceptJSONDecode,
)

from oracle_voter.common.client import HttpError, http_get, http_post


@patch("oracle_voter.common.client.aiohttp")
def test_200_OK(mock):
    url = "http://google.com"
    mock.ClientSession = SessionOk
    resp_body = {"hello": "world"}
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(http_get(url))
    assert result == resp_body


@patch("oracle_voter.common.client.aiohttp")
def test_404_NOTFOUND(mock):
    url = "http://google.com"
    mock.ClientSession = Session404
    loop = asyncio.get_event_loop()
    with pytest.raises(HttpError):
        loop.run_until_complete(http_get(url))


@patch("oracle_voter.common.client.aiohttp")
def test_except_client_connection(mock):
    url = "http://google.com"
    mock.ClientSession = SessionExceptClientConnection
    loop = asyncio.get_event_loop()
    with pytest.raises(HttpError):
        loop.run_until_complete(http_get(url))


@patch("oracle_voter.common.client.aiohttp")
def test_except_server_timeout(mock):
    url = "http://google.com"
    mock.ClientSession = SessionExceptServerTimeout
    loop = asyncio.get_event_loop()
    with pytest.raises(HttpError):
        loop.run_until_complete(http_get(url))


@patch("oracle_voter.common.client.aiohttp")
def test_except_json_decode(mock):
    url = "http://google.com"
    mock.ClientSession = SessionExceptJSONDecode
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(http_get(url))
    assert result is None


@patch("oracle_voter.common.client.aiohttp")
def test_POST_404_NOTFOUND(mock):
    url = "http://google.com"
    mock.ClientSession = Session404
    loop = asyncio.get_event_loop()
    with pytest.raises(HttpError):
        loop.run_until_complete(http_post(url))


@patch("oracle_voter.common.client.aiohttp")
def test_post_except_client_connection(mock):
    url = "http://google.com"
    mock.ClientSession = SessionExceptClientConnection
    loop = asyncio.get_event_loop()
    with pytest.raises(HttpError):
        loop.run_until_complete(http_post(url))


@patch("oracle_voter.common.client.aiohttp")
def test_post_except_server_timeout(mock):
    url = "http://google.com"
    mock.ClientSession = SessionExceptServerTimeout
    loop = asyncio.get_event_loop()
    with pytest.raises(HttpError):
        loop.run_until_complete(http_post(url))


@patch("oracle_voter.common.client.aiohttp")
def test_post_except_json_decode(mock):
    url = "http://google.com"
    mock.ClientSession = SessionExceptJSONDecode
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(http_post(url))
    assert result is None
