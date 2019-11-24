from common import client
import pytest
import asyncio
from aioresponses import aioresponses


@pytest.fixture
def http_get_client():
    return client.http_get


@pytest.fixture
def get_loop():
    return asyncio.get_event_loop()


@pytest.fixture
def http_mock():
    m = aioresponses()
    m.start()
    return m
