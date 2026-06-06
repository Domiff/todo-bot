from datetime import datetime
from string import Template

from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from bot.auth.service import auth_service
from bot.core.http import HttpClient, TodoURL, http_client


class TodoService:
    def __init__(self):
        self.client: HttpClient = http_client()

    async def create_task(self, access: str, refresh: str, state: FSMContext, task: dict):
        headers = {"Authorization": f"Bearer {access}"}
        async with self.client as client:
            data = await client.post(TodoURL.CREATE, data=task, headers=headers)
            if data[1] == 401:
                headers = await auth_service.check_token(refresh, state)
                data = await client.post(TodoURL.CREATE, data=task, headers=headers)
            return data

    async def get_tasks(self, access: str, refresh: str, state: FSMContext) -> list:
        headers = {"Authorization": f"Bearer {access}"}
        async with self.client as client:
            data = await client.get(TodoURL.LIST, headers=headers)
            if data[1] == 401 or not data:
                headers = await auth_service.check_token(refresh, state)
            data = await client.get(TodoURL.LIST, headers=headers)
            return data[0]

    async def update_task(self, access: str, refresh: str, state: FSMContext, task: dict, pk: int):
        headers = {"Authorization": f"Bearer {access}"}
        async with self.client as client:
            data = await client.patch(TodoURL.UPDATE, pk=pk, data=task, headers=headers)
            if data[1] == 401:
                headers = await auth_service.check_token(refresh, state)
                data = await client.patch(TodoURL.UPDATE, pk=pk, data=task, headers=headers)
            return data

    async def delete_task(self, access: str, refresh: str, state: FSMContext, pk: int):
        headers = {"Authorization": f"Bearer {access}"}
        async with self.client as client:
            data = await client.delete(TodoURL.DELETE, pk=pk, headers=headers)
            if data == 401:
                headers = await auth_service.check_token(refresh, state)
                data = await client.delete(TodoURL.DELETE, pk=pk, headers=headers)
            return data

    async def prepare_message(self, access: str, refresh: str, state: FSMContext) -> list[str]:
        data = await self.get_tasks(access, refresh, state)
        if not data:
            return ["You not have any tasks"]
        messages = []
        for item in data:
            deadline = datetime.fromisoformat(item["deadline"]).strftime("%d.%m.%Y %H:%M")
            created_at = datetime.fromisoformat(item["created_at"]).strftime("%d.%m.%Y %H:%M")
            messages.append(
                Template(
                    f"{markdown.hbold('Title')}: $title\n"
                    f"{markdown.hbold('Body')}: $body \n"
                    f"{markdown.hbold('Deadline')}: $deadline\n"
                    f"{markdown.hbold('Created_at')}: $created_at\n"
                    f"{markdown.hbold('Category')}: $category\n",
                ).substitute(
                    title=item["title"],
                    deadline=deadline,
                    body=item["body"],
                    created_at=created_at,
                    category=item["category"],
                ),
            )
        return messages


todo_service = TodoService()
