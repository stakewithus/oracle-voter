from common import client


class Base:

    def __init__(self, api_url):
        self.api_url = api_url
        self.client = client
