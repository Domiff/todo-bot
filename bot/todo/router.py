from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from .dialog import create_dialog, delete_dialog, read_dialog, update_dialog
from .states import CreateStates, DeleteStates, ReadState, UpdateState

router = Router()
router.include_routers(read_dialog, create_dialog, update_dialog, delete_dialog)


@router.message(Command("show_tasks"))
async def show_tasks(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await dialog_manager.start(state=ReadState.read, mode=StartMode.RESET_STACK)


@router.message(Command("create_task"))
async def create_task_command(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await dialog_manager.start(state=CreateStates.title, mode=StartMode.RESET_STACK)


@router.message(Command("update_task"))
async def update_task_command(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await dialog_manager.start(state=UpdateState.choose_task, mode=StartMode.RESET_STACK)


@router.message(Command("delete_task"))
async def delete_task_command(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await dialog_manager.start(state=DeleteStates.choose_task, mode=StartMode.RESET_STACK)
