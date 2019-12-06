import aiohttp
import simplejson as json
from simplejson.errors import JSONDecodeError
from aiohttp.client_exceptions import ClientConnectionError


class HttpError(Exception):
    def __init__(self, message, status_code, result):
        super().__init__(message)
        self.status_code = status_code
        self.result = result


async def http_get(url, params=dict()):
    result = {}
    session = aiohttp.ClientSession()
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=2, sock_read=2)
    try:
        #
        http_resp = await session.get(url, params=params, timeout=timeout)
        status_code = http_resp.status
        raw_text = await http_resp.text()
        if len(raw_text) > 0:
            result = json.loads(raw_text)
        if status_code != 200:
            raise HttpError(f"Url: {url}", status_code, result)
        await session.close()
        return result
    except JSONDecodeError:
        # Problems decoding JSON
        await session.close()
        return None
    except (HttpError, ClientConnectionError) as err:
        await session.close()
        raise err


async def http_post(url, params=dict(), post_data=dict()):
    result = {}
    session = aiohttp.ClientSession()
    try:
        #
        http_resp = await session.post(url, params=params, data=post_data)
        status_code = http_resp.status
        raw_text = await http_resp.text()
        if len(raw_text) > 0:
            result = json.loads(raw_text)
        if status_code != 200:
            raise HttpError(f"Url: {url}", status_code, result)
        await session.close()
        return result
    except JSONDecodeError:
        # Problems decoding JSON
        await session.close()
        return None
    except (HttpError, ClientConnectionError) as err:
        await session.close()
        raise err
