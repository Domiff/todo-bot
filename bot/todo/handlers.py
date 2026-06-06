from datetime import datetime
from typing import TYPE_CHECKING

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from bot.todo.service import todo_service

from .states import UpdateState

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext


class CreateHandlers:
    @staticmethod
    async def title(
        message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, value: str,
    ) -> None:
        dialog_manager.dialog_data["title"] = value
        await dialog_manager.next()

    @staticmethod
    async def body(
        message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, value: str,
    ) -> None:
        dialog_manager.dialog_data["body"] = value
        await dialog_manager.next()

    @staticmethod
    async def deadline(
        message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, value: str,
    ) -> None:
        dialog_manager.dialog_data["deadline"] = value
        await dialog_manager.next()

    @staticmethod
    async def category(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
        dialog_manager.dialog_data["category"] = button.widget_id.capitalize()
        await dialog_manager.next()

    @staticmethod
    async def confirm(callback: CallbackQuery, button, dialog_manager: DialogManager):
        state: FSMContext = dialog_manager.middleware_data["state"]
        tokens = await state.get_data()
        task = {
            "title": dialog_manager.dialog_data["title"],
            "body": dialog_manager.dialog_data["body"],
            "category": dialog_manager.dialog_data["category"],
            "deadline": datetime.strptime(
                dialog_manager.dialog_data["deadline"], "%d.%m.%Y %H:%M",
            ).isoformat(),
        }
        await todo_service.create_task(tokens.get("access"), tokens.get("refresh"), state, task)
        await callback.message.answer("Task created successfully.")
        await dialog_manager.done()


class ReadHandlers:
    @staticmethod
    async def get_tasks(callback: CallbackQuery, button, dialog_manager: DialogManager) -> None:
        state: FSMContext = dialog_manager.middleware_data["state"]
        tokens = await state.get_data()
        tasks = await todo_service.prepare_message(tokens.get("access"), tokens.get("refresh"), state)
        for task in tasks:
            await callback.message.answer(task)
        await dialog_manager.done()

    @staticmethod
    async def tasks_getter(dialog_manager: DialogManager, **kwargs):
        state = dialog_manager.middleware_data["state"]
        tokens = await state.get_data()
        tasks = await todo_service.get_tasks(tokens["access"], tokens["refresh"], state)
        return {"tasks": tasks}


class UpdateHandlers:
    @staticmethod
    async def choose_task(
        callback: CallbackQuery, widget: ManagedTextInput, dialog_manager: DialogManager, item_id: str,
    ):
        dialog_manager.dialog_data["task_id"] = int(item_id)
        await dialog_manager.next()

    @staticmethod
    async def choose_field(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
        match button.widget_id:
            case "task_title":
                await dialog_manager.switch_to(state=UpdateState.title)
            case "task_body":
                await dialog_manager.switch_to(state=UpdateState.body)
            case "task_deadline":
                await dialog_manager.switch_to(state=UpdateState.deadline)

    @staticmethod
    async def edit_title(
        message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, value: str,
    ):
        dialog_manager.dialog_data["title"] = value
        await dialog_manager.next()

    @staticmethod
    async def edit_body(
        message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, value: str,
    ):
        dialog_manager.dialog_data["body"] = value
        await dialog_manager.next()

    @staticmethod
    async def edit_deadline(
        message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, value: str,
    ):
        dialog_manager.dialog_data["deadline"] = value
        await dialog_manager.next()

    @staticmethod
    async def edit_category(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
        dialog_manager.dialog_data["category"] = button.widget_id.capitalize()
        await dialog_manager.next()

    @staticmethod
    async def confirm(callback: CallbackQuery, widget, dialog_manager: DialogManager):
        state: FSMContext = dialog_manager.middleware_data["state"]
        tokens = await state.get_data()
        pk = int(dialog_manager.dialog_data["task_id"])
        task = {
            key: val
            for key, val in {
                "title": dialog_manager.dialog_data.get("title"),
                "body": dialog_manager.dialog_data.get("body"),
                "deadline": (
                    datetime.strptime(
                        dialog_manager.dialog_data["deadline"], "%d.%m.%Y %H:%M",
                    ).isoformat()
                    if dialog_manager.dialog_data.get("deadline")
                    else None
                ),
            }.items()
            if val
        }
        await todo_service.update_task(tokens.get("access"), tokens.get("refresh"), state, task, pk)
        await callback.message.answer("Task updated successfully.")
        await dialog_manager.done()

    @staticmethod
    async def cancel(callback: CallbackQuery, widget, dialog_manager: DialogManager):
        await callback.message.answer("Cancelling.")
        await dialog_manager.done()


class DeleteHandlers:
    @staticmethod
    async def choose_task(
        callback: CallbackQuery, widget: ManagedTextInput, dialog_manager: DialogManager, item_id: str,
    ):
        dialog_manager.dialog_data["task_id"] = int(item_id)
        await dialog_manager.next()

    @staticmethod
    async def confirm(callback: CallbackQuery, widget, dialog_manager: DialogManager):
        state: FSMContext = dialog_manager.middleware_data["state"]
        tokens = await state.get_data()
        pk = int(dialog_manager.dialog_data["task_id"])
        await todo_service.delete_task(tokens.get("access"), tokens.get("refresh"), state, pk)
        await callback.message.answer("Task deleted")
        await dialog_manager.done()
