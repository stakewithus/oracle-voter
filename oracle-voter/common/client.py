import aiohttp
import simplejson as json


class HttpError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


async def http_get(url, params=dict()):
    result = {}
    session = aiohttp.ClientSession()
    try:
        #
        http_resp = await session.get(url, params=params)
        status_code = http_resp.status
        if status_code != 200:
            raise HttpError(f"Url: {url}", status_code)
        raw_text = await http_resp.text()
        result = json.loads(raw_text)
        await session.close()
        return result
    except (HttpError,) as err:
        if isinstance(err, HttpError):
            await session.close()
            raise err
