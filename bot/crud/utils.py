from aiogram.fsm.context import FSMContext

from bot.api import AuthClient, Urls


async def refresh_token(refresh, state: FSMContext):
    async with AuthClient(Urls.BASE_URL) as client:
        data = await client.post(Urls.REFRESH, payload=refresh)
        new_access = data.get("access")
        await state.update_data(access=new_access)
        return new_access


async def check_token(refresh, state):
    refresh_token_dict = {
        "refresh": refresh,
    }
    new_access = await refresh_token(refresh_token_dict, state)
    if not new_access:
        return ["You are need log in"]
    headers = {"Authorization": f"Bearer {new_access}"}
    return headers
