from ..api import AuthClient, Urls


async def register(user):
    payload = {
        "tg_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
    async with AuthClient(Urls.BASE_URL) as client:
        data = await client.post(Urls.REGISTER, payload)
        return data
