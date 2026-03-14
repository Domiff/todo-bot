from datetime import datetime
from string import Template

from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from bot.api import ApiClient, urls_dict
from bot.crud.utils import check_token


async def get_tasks(access: str, refresh: str, state: FSMContext):
    headers = {"Authorization": f"Bearer {access}"}
    async with ApiClient(urls_dict.get("base_url")) as client:
        data = await client.get(urls_dict.get("read"), headers=headers)
        code = data[1]
        if code == 401 or not data:
            headers = await check_token(refresh, state)
        data = await client.get(urls_dict.get("read"), headers=headers)
        return data[0]


async def prepare_message(access: str, refresh: str, state):
    data = await get_tasks(access, refresh, state)
    message_for_user = []
    if len(data) == 0:
        message_for_user = ["You dont have any tasks"]
        return message_for_user
    for i in range(len(data)):
        title = data[i]["title"]
        deadline = datetime.fromisoformat(data[i]["deadline"]).strftime(
            "%d.%m.%Y %H:%M",
        )
        body = data[i]["body"]
        created_at = datetime.fromisoformat(data[i]["created_at"]).strftime(
            "%d.%m.%Y %H:%M",
        )
        category = data[i]["category"]
        message_for_user += [
            Template(
                f"{markdown.hbold('Title')}: $title\n"
                f"{markdown.hbold('Body')}: $body \n"
                f"{markdown.hbold('Deadline')}: $deadline\n"
                f"{markdown.hbold('Created_at')}: $created_at\n"
                f"{markdown.hbold('Category')}: $category\n",
            ).substitute(
                title=title,
                deadline=deadline,
                body=body,
                created_at=created_at,
                category=category,
            ),
        ]
    return message_for_user
