from aiogram.fsm.context import FSMContext

from bot.api import ApiClient, Urls
from bot.crud.utils import check_token


async def create_task(access: str, refresh: str, state: FSMContext, task: dict):
    headers = {"Authorization": f"Bearer {access}"}
    async with ApiClient(Urls.BASE_URL) as client:
        data = await client.post(Urls.CREATE, headers=headers, data=task)
        code = data[1]
        if code == 401:
            headers = await check_token(refresh, state)
            data = await client.post(
                Urls.CREATE, headers=headers, data=task,
            )
        return data
