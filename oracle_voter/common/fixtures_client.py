from aiohttp.client_exceptions import ClientConnectionError, ServerTimeoutError


class DummySession:

    async def get(self, *args, **kwargs):
        pass

    async def post(self, *args, **kwargs):
        pass

    async def close(self, *args, **kwargs):
        pass


class DummySessionResult:

    def __init__(self, status, raw_text):
        self.status = status
        self.raw_text = raw_text

    async def text(self):
        return self.raw_text


class SessionOk(DummySession):

    async def get(self, *args, **kwargs):
        return DummySessionResult(
            200,
            """{"hello": "world"}"""
        )


class Session404(DummySession):

    async def get(self, *args, **kwargs):
        return DummySessionResult(
            404,
            """"""
        )

    async def post(self, *args, **kwargs):
        return DummySessionResult(
            404,
            """"""
        )


class SessionExceptClientConnection(DummySession):

    async def get(self, *args, **kwargs):
        raise ClientConnectionError()

    async def post(self, *args, **kwargs):
        raise ClientConnectionError()


class SessionExceptServerTimeout(DummySession):

    async def get(self, *args, **kwargs):
        raise ServerTimeoutError()

    async def post(self, *args, **kwargs):
        raise ServerTimeoutError()


class SessionExceptJSONDecode(DummySession):

    async def get(self, *args, **kwargs):
        return DummySessionResult(
            200,
            """{h"""
        )

    async def post(self, *args, **kwargs):
        return DummySessionResult(
            200,
            """{h"""
        )
