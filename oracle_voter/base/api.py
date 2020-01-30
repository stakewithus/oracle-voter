# -----------------------------------------------------------------------------
import aiohttp
import simplejson as json
from aiohttp.client_exceptions import (
    ClientConnectionError,
    ServerTimeoutError,
    ClientConnectorError
)

from yarl import URL

from oracle_voter.base.errors import HttpError

# -----------------------------------------------------------------------------


class API:

    base_url = None
    session = None
    timeout = None

    # Timeout Settings
    timeout_sock_connect = 2
    timeout_sock_read = 2

    def __init__(self, config={}):

        self.base_url = URL(config.get('base_url', self.base_url))

        self.timeout_sock_connect = config.get(
            'timeout_sock_connect',
            self.timeout_sock_connect
        )

        self.timeout_sock_read = config.get(
            'timeout_sock_read',
            self.timeout_sock_read
        )
        self.timeout = aiohttp.ClientTimeout(
            total=None,
            sock_connect=self.timeout_sock_connect,
            sock_read=self.timeout_sock_read
        )

    def open(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close(self):
        if self.session is None:
            await self.session.close()

    def _parse_json(self, http_response):
        try:
            return json.loads(http_response)
        except ValueError:  # JSONDecodeError
            pass

    async def fetch(
        self,
        url,
        method='GET',
        headers=None,
        body=None,
        query=None
    ):
        encoded_body = body.encode() if body else None

        self.open()
        session_method = getattr(self.session, method.lower())

        http_response = None
        http_status_code = None
        json_response = None
        target_url = self.base_url.parent / url

        try:
            async with session_method(
                target_url,
                params=query,
                data=encoded_body,
                timeout=self.timeout
            ) as response:
                http_status_code = response.status
                http_response = await response.text()
                json_response = self._parse_json(http_response)

        except (
            ServerTimeoutError,
            ClientConnectionError,
            ClientConnectorError,
        ):
            raise HttpError(f"({method})[{http_status_code}]: {url}")

        if json_response is not None:
            return json_response
