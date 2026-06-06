from typing import TYPE_CHECKING

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from bot.crud import prepare_message

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext


async def get_tasks_handler(
    callback: CallbackQuery, button, dialog_manager: DialogManager,
) -> None:
    state: FSMContext = dialog_manager.middleware_data["state"]
    data = await state.get_data()
    access = data.get("access")
    refresh = data.get("refresh")
    tasks = await prepare_message(access, refresh, state)
    for task in tasks:
        await callback.message.answer(task)
    await dialog_manager.done()
