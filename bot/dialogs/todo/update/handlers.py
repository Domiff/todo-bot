from datetime import datetime
from typing import TYPE_CHECKING

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from bot.crud import update_task

from .states import UpdateState

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext


async def choose_task_handler(
    callback: CallbackQuery,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data["task_id"] = int(item_id)
    await dialog_manager.next()


async def choose_filed_handler(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    match button.widget_id:
        case "task_title":
            await dialog_manager.switch_to(state=UpdateState.title)
        case "task_body":
            await dialog_manager.switch_to(state=UpdateState.body)
        case "task_deadline":
            await dialog_manager.switch_to(state=UpdateState.deadline)


async def edit_title_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data["title"] = value
    await dialog_manager.next()


async def edit_body_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data["body"] = value
    await dialog_manager.next()


async def edit_deadline_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data["deadline"] = value
    await dialog_manager.next()


async def edit_category_handler(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    match button.widget_id:
        case "primary":
            dialog_manager.dialog_data["category"] = "Primary"
        case "secondary":
            dialog_manager.dialog_data["category"] = "Secondary"
    await dialog_manager.next()


async def confirm_handler(
    callback: CallbackQuery,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
):
    state: FSMContext = dialog_manager.middleware_data["state"]
    tokens = await state.get_data()
    access = tokens.get("access")
    refresh = tokens.get("refresh")

    pk = int(dialog_manager.dialog_data["task_id"])

    title = dialog_manager.dialog_data.get("title") if True else None
    body = dialog_manager.dialog_data.get("body") if True else None
    deadline = dialog_manager.dialog_data.get("deadline")
    if dialog_manager.dialog_data.get("deadline"):
        deadline = (
            datetime.strptime(
                dialog_manager.dialog_data.get("deadline"), "%d.%m.%Y %H:%M",
            ).isoformat()
            if True
            else None
        )
    task = {
        "title": title,
        "body": body,
        "deadline": deadline,
    }

    keys_for_drops = []
    for key, value in task.items():
        if not value:
            keys_for_drops.append(key)

    for i in range(len(keys_for_drops)):
        task.pop(keys_for_drops[i])

    await update_task(access, refresh, state, task, pk)
    await callback.message.answer("Task updated successfully.")
    await dialog_manager.done()


async def cancel_handler(
    callback: CallbackQuery,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
):
    await callback.message.answer("Cancelling.")
    await dialog_manager.done()
