from bot.api import ApiClient, urls_dict
from bot.crud.utils import check_token


async def delete_task(access, refresh, state, pk):
    headers = {"Authorization": f"Bearer {access}"}
    async with ApiClient(urls_dict.get("base_url")) as client:
        data = await client.delete(urls_dict.get("delete"), headers=headers, pk=pk)
        if data == 401:
            headers = await check_token(refresh, state)
            data = await client.delete(urls_dict.get("delete"), headers=headers, pk=pk)
        return data
