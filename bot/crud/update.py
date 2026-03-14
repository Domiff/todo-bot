from aiogram.fsm.context import FSMContext

from bot.api import ApiClient, urls_dict
from bot.crud.utils import check_token


async def update_task(
    access: str, refresh: str, state: FSMContext, task: dict, pk: int,
):
    headers = {"Authorization": f"Bearer {access}"}
    async with ApiClient(urls_dict.get("base_url")) as client:
        data = await client.patch(
            urls_dict.get("update"), headers=headers, data=task, pk=pk,
        )
        code = data[1]
        if code == 401:
            headers = await check_token(refresh, state)
            data = await client.patch(
                urls_dict.get("update"), headers=headers, data=task, pk=pk,
            )
        return data
