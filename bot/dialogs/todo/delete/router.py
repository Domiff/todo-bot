from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from .dialog import delete_dialog
from .states import DeleteStates

router = Router()
router.include_router(delete_dialog)


@router.message(Command("delete_task"))
async def delete_task_command(
    message: Message, dialog_manager: DialogManager, state: FSMContext,
):
    await dialog_manager.start(
        state=DeleteStates.choose_task, mode=StartMode.RESET_STACK,
    )
