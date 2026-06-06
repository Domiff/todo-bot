from enum import StrEnum

import aiohttp

from bot.core.config import settings


class AuthURL(StrEnum):
    REGISTER = "auth/tg/register/"
    REFRESH = "auth/token/refresh/"


class TodoURL(StrEnum):
    LIST = "api/list/"
    CREATE = "api/create/"
    UPDATE = "api/update/"
    DELETE = "api/delete/"


class HttpClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(ssl=False)
        self.session = aiohttp.ClientSession(base_url=self.base_url, connector=connector)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def get(self, url: str, headers: dict = None, pk: int = None):
        if pk:
            url += str(pk)
        async with self.session.get(url, headers=headers) as response:
            return await response.json(), response.status

    async def post(self, url: str, data: dict = None, json: dict = None, headers: dict = None):
        async with self.session.post(url, data=data, json=json, headers=headers) as response:
            return await response.json(), response.status

    async def patch(self, url: str, pk: int, data: dict, headers: dict = None):
        url += str(pk)
        async with self.session.patch(url, data=data, headers=headers) as response:
            return await response.json(), response.status

    async def delete(self, url: str, pk: int, headers: dict = None):
        url += str(pk)
        async with self.session.delete(url, headers=headers) as response:
            return response.status


def http_client() -> HttpClient:
    return HttpClient(settings.BASE_URL)
