from common import client
import pytest


@pytest.fixture
def http_get_client():
    return client.http_get
