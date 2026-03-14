from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from .dialog import create_dialog
from .states import CreateStates

router = Router()
router.include_router(create_dialog)


@router.message(Command("create_task"))
async def create_task_command(
    message: Message, dialog_manager: DialogManager, state: FSMContext,
):
    await dialog_manager.start(state=CreateStates.title, mode=StartMode.RESET_STACK)
