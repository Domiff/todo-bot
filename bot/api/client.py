import aiohttp


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(ssl=False)
        self.session = aiohttp.ClientSession(base_url=self.base_url, connector=connector)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


class ApiClient(Client):
    async def get(self, url: str, headers: dict, pk: int = None):
        if pk:
            url += str(pk)
        async with self.session.get(url, headers=headers) as response:
            return await response.json(), response.status

    async def post(self, url: str, data: dict, headers: dict):
        async with self.session.post(url, data=data, headers=headers) as response:
            return await response.json(), response.status

    async def put(self, url: str, pk: int, data: dict, headers: dict):
        url += str(pk)
        async with self.session.put(url, data=data, headers=headers) as response:
            return await response.json(), response.status

    async def patch(self, url: str, pk: int, data: dict, headers: dict):
        url += str(pk)
        async with self.session.patch(url, data=data, headers=headers) as response:
            return await response.json(), response.status

    async def delete(self, url: str, pk, headers: dict):
        url += str(pk)
        async with self.session.delete(url, headers=headers) as response:
            return response.status


class AuthClient(Client):
    async def post(self, url: str, payload: dict):
        async with self.session.post(url, json=payload) as client:
            return await client.json()
