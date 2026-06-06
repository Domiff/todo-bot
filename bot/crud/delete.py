from bot.api import ApiClient, Urls
from bot.crud.utils import check_token


async def delete_task(access, refresh, state, pk):
    headers = {"Authorization": f"Bearer {access}"}
    async with ApiClient(Urls.BASE_URL) as client:
        data = await client.delete(Urls.DELETE, headers=headers, pk=pk)
        if data == 401:
            headers = await check_token(refresh, state)
            data = await client.delete(Urls.DELETE, headers=headers, pk=pk)
        return data
