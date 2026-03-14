from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from .dialog import update_dialog
from .states import UpdateState

router = Router()
router.include_router(update_dialog)


@router.message(Command("update_task"))
async def update_router(
    message: Message, dialog_manager: DialogManager, state: FSMContext,
):
    await dialog_manager.start(
        state=UpdateState.choose_task, mode=StartMode.RESET_STACK,
    )
