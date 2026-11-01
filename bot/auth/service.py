import aiohttp
from aiogram.fsm.context import FSMContext

from bot.auth.exceptions import UNAVAILABLE, AuthError, TokenExpired
from bot.core.config import settings
from bot.core.http import AuthURL, HttpClient, http_client


def first_error(data: dict) -> str:
    for field in ("username", "password", "email", "tg_id", "detail"):
        value = data.get(field)
        if value:
            return value[0] if isinstance(value, list) else str(value)
    return UNAVAILABLE


class AuthService:
    def __init__(self):
        self.client: HttpClient = http_client()

    async def register(self, username: str, password: str, tg_id: int) -> dict:
        payload = {"username": username, "password": password, "tg_id": tg_id}
        headers = {"X-Bot-Key": settings.BOT_API_KEY}
        try:
            async with self.client as client:
                data, status = await client.post(
                    AuthURL.REGISTER, json=payload, headers=headers
                )
        except aiohttp.ClientError as error:
            raise AuthError(UNAVAILABLE) from error
        if status != 201:
            raise AuthError(first_error(data))
        return data["tokens"]

    async def login(self, username: str, password: str, tg_id: int) -> dict:
        credentials = {"username": username, "password": password}
        try:
            async with self.client as client:
                tokens, status = await client.post(AuthURL.TOKEN, json=credentials)
                if status == 401:
                    raise AuthError("Incorrect username or password.")
                if status != 200:
                    raise AuthError(first_error(tokens))

                data, status = await client.post(
                    AuthURL.TG_LINK,
                    json={"tg_id": tg_id},
                    headers={
                        "Authorization": f"Bearer {tokens['access']}",
                        "X-Bot-Key": settings.BOT_API_KEY,
                    },
                )
        except aiohttp.ClientError as error:
            raise AuthError(UNAVAILABLE) from error
        if status != 200:
            raise AuthError(first_error(data))
        return tokens

    async def refresh_token(self, refresh: str, state: FSMContext) -> str | None:
        try:
            async with self.client as client:
                data, _ = await client.post(AuthURL.REFRESH, json={"refresh": refresh})
        except aiohttp.ClientError:
            return None
        new_access = data.get("access")
        await state.update_data(access=new_access, refresh=data.get("refresh"))
        return new_access

    async def check_token(self, refresh: str, state: FSMContext) -> dict:
        new_access = await self.refresh_token(refresh, state)
        if not new_access:
            raise TokenExpired
        return {"Authorization": f"Bearer {new_access}"}


auth_service = AuthService()
