import aiohttp
import simplejson as json


class HttpError(Exception):
    def __init__(self, message, status_code, result):
        super().__init__(message)
        self.status_code = status_code
        self.result = result


async def http_get(url, params=dict()):
    result = {}
    session = aiohttp.ClientSession()
    try:
        #
        http_resp = await session.get(url, params=params)
        status_code = http_resp.status
        raw_text = await http_resp.text()
        # print(result)
        if len(raw_text) > 0:
            result = json.loads(raw_text)
        if status_code != 200:
            raise HttpError(f"Url: {url}", status_code, result)
        await session.close()
        return result
    except (HttpError,) as err:
        if isinstance(err, HttpError):
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
    except (HttpError,) as err:
        if isinstance(err, HttpError):
            await session.close()
            raise err
