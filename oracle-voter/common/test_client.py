import pytest
from common.client import HttpError
from aioresponses import aioresponses
import asyncio


def test_200_OK(http_get_client):
    url = "http://google.com"
    loop = asyncio.get_event_loop()
    with aioresponses() as m:
        resp_body = {"hello": "world"}
        m.get(url, status=200, payload=resp_body)

        result = loop.run_until_complete(http_get_client(url))
        assert result == resp_body


def test_404_NOTFOUND(http_get_client):
    url = "http://google.com"
    loop = asyncio.get_event_loop()
    with aioresponses() as m:
        m.get(url, status=404)
        with pytest.raises(HttpError):
            loop.run_until_complete(http_get_client(url))
