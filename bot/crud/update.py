from aiogram.fsm.context import FSMContext

from bot.api import ApiClient, Urls
from bot.crud.utils import check_token


async def update_task(
    access: str, refresh: str, state: FSMContext, task: dict, pk: int,
):
    headers = {"Authorization": f"Bearer {access}"}
    async with ApiClient(Urls.BASE_URL) as client:
        data = await client.patch(
            Urls.UPDATE, headers=headers, data=task, pk=pk,
        )
        code = data[1]
        if code == 401:
            headers = await check_token(refresh, state)
            data = await client.patch(
                Urls.UPDATE, headers=headers, data=task, pk=pk,
            )
        return data
