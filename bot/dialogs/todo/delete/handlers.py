from typing import TYPE_CHECKING

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from bot.crud.delete import delete_task

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
    await delete_task(access, refresh, state, pk)
    await callback.message.answer("Task deleted")
    await dialog_manager.done()
