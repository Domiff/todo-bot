from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from .dialog import auth_dialog
from .handlers import COMMANDS
from .states import AuthState

router = Router()
router.include_router(auth_dialog)


@router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager, state: FSMContext):
    tokens = await state.get_data()
    if tokens.get("refresh"):
        await message.answer(f"You are already logged in\n{COMMANDS}")
        return
    await dialog_manager.start(state=AuthState.choose, mode=StartMode.RESET_STACK)
