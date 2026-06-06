from ..api import AuthClient, urls_dict


async def register(user):
    payload = {
        "tg_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
    async with AuthClient(urls_dict.get("base_url")) as client:
        data = await client.post(urls_dict.get("register"), payload)
        return data
