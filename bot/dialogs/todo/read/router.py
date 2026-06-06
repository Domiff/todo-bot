from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from .dialog import read_dialog
from .states import ReadState

router = Router()
router.include_router(read_dialog)


@router.message(Command("show_tasks"))
async def show_tasks(
    message: Message, dialog_manager: DialogManager, state: FSMContext,
):
    await dialog_manager.start(state=ReadState.read, mode=StartMode.RESET_STACK)
