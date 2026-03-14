from typing import TYPE_CHECKING

from aiogram.types import CallbackQuery
from aiogram.utils import markdown
from aiogram_dialog import DialogManager

from bot.register import register

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext


async def confirm_registration(
    callback: CallbackQuery, button, dialog_manager: DialogManager,
) -> None:
    user = callback.from_user
    data = await register(user)
    access = data["tokens"]["access"]
    refresh = data["tokens"]["refresh"]
    tokens_dict = {"access": access, "refresh": refresh}
    state: FSMContext = dialog_manager.middleware_data["state"]
    await state.update_data(tokens_dict)
    await callback.message.answer(
        f"You registered\n"
        f"{markdown.hcode('/show_tasks')}\n"
        f"{markdown.hcode('/create_task')}\n"
        f"{markdown.hcode('/update_task')}\n"
        f"{markdown.hcode('/delete_task')}\n",
    )
    await dialog_manager.done()
