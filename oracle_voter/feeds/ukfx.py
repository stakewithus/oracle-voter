from oracle_voter.feeds.base import Base
from oracle_voter.common import client


class UKFX(Base):

    def __init__(self, api_url):
        super().__init__(api_url)

    async def get_swap(self, base_currency, swap_currency):
        target_url = f"{self.api_url}/pairs/{base_currency}/{swap_currency}/livehistory/chart?t=1"
        http_res = await client.http_get(target_url)
        # Get Most Recent Price
        if http_res is None:
            return "-1.00"
        if len(http_res) > 0:
            last_update = http_res[(len(http_res) - 1)]
            raw_px = last_update[1]
            return raw_px
