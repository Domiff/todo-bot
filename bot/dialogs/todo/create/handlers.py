from datetime import datetime
from typing import TYPE_CHECKING

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from bot.crud import create_task

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext


async def title_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    value: str,
) -> None:
    dialog_manager.dialog_data["title"] = value
    await dialog_manager.next()


async def body_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    value: str,
) -> None:
    dialog_manager.dialog_data["body"] = value
    await dialog_manager.next()


async def deadline_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    value: str,
) -> None:
    dialog_manager.dialog_data["deadline"] = value
    await dialog_manager.next()


async def category_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    value: str,
) -> None:
    dialog_manager.dialog_data["category"] = value
    await dialog_manager.next()


async def primary_handler(
    callback: CallbackQuery, button, dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["category"] = "Primary"
    await dialog_manager.next()


async def secondary_handler(
    callback: CallbackQuery, button, dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["category"] = "Secondary"
    await dialog_manager.next()


async def confirm_create_handler(
    callback: CallbackQuery, button, dialog_manager: DialogManager,
):
    state: FSMContext = dialog_manager.middleware_data["state"]
    tokens = await state.get_data()
    access = tokens.get("access")
    refresh = tokens.get("refresh")
    title = dialog_manager.dialog_data["title"]
    body = dialog_manager.dialog_data["body"]
    category = dialog_manager.dialog_data["category"]
    deadline = datetime.strptime(
        dialog_manager.dialog_data["deadline"], "%d.%m.%Y %H:%M",
    ).isoformat()
    task = {
        "title": title,
        "body": body,
        "deadline": deadline,
        "category": category,
    }
    await create_task(access, refresh, state, task)
    await callback.message.answer("Task created successfully.")
    await dialog_manager.done()
