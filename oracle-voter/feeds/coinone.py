from feeds.base import Base
from common import client


class Coinone(Base):

    def __init__(self, api_url):
        super().__init__(api_url)

    def postpro_trades(self, http_res):
        pass

    async def get_trades(self, currency):
        get_params = {"currency": currency, "format": "json"}
        target_url = f"{self.api_url}/trades/"
        http_res = await client.http_get(target_url, params=get_params)
        return self.postpro_trades(http_res)
