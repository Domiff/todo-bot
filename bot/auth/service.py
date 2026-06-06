from aiogram.fsm.context import FSMContext

from bot.core.http import AuthURL, HttpClient, http_client


class AuthService:
    def __init__(self):
        self.client: HttpClient = http_client()

    async def register(self, user) -> dict:
        payload = {
            "tg_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        async with self.client as client:
            data, _ = await client.post(AuthURL.REGISTER, json=payload)
            return data

    async def refresh_token(self, refresh: str, state: FSMContext) -> str | None:
        async with self.client as client:
            data, _ = await client.post(AuthURL.REFRESH, json={"refresh": refresh})
            new_access = data.get("access")
            await state.update_data(access=new_access)
            return new_access

    async def check_token(self, refresh: str, state: FSMContext) -> dict | list:
        new_access = await self.refresh_token(refresh, state)
        if not new_access:
            return ["You are need log in"]
        return {"Authorization": f"Bearer {new_access}"}


auth_service = AuthService()
