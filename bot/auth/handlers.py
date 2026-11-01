import html
import logging
from typing import TYPE_CHECKING

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, ErrorEvent, Message
from aiogram.utils import markdown
from aiogram_dialog import DialogManager, ShowMode

from bot.auth.exceptions import AuthError
from bot.auth.service import auth_service

from .states import AuthState

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)

COMMANDS = (
    f"{markdown.hcode('/show_tasks')}\n"
    f"{markdown.hcode('/create_task')}\n"
    f"{markdown.hcode('/update_task')}\n"
    f"{markdown.hcode('/delete_task')}\n"
)


async def delete_message(message: Message) -> None:
    try:
        await message.delete()
    except TelegramBadRequest:
        logger.warning("Failed to delete credentials message")


async def delete_prompt(message: Message, message_id: int | None) -> None:
    if message_id is None:
        return
    try:
        await message.bot.delete_message(message.chat.id, message_id)
    except TelegramBadRequest:
        logger.warning("Failed to delete credentials prompt")


async def token_expired(event: ErrorEvent) -> None:
    update = event.update
    message = update.message or update.callback_query.message
    await message.answer("Your session has expired. Send /start to log in again.")


class AuthHandlers:
    @staticmethod
    async def getter(dialog_manager: DialogManager, **kwargs) -> dict:
        return {"error": dialog_manager.dialog_data.get("error", "")}

    @staticmethod
    async def choose(
        callback: CallbackQuery, button, dialog_manager: DialogManager
    ) -> None:
        dialog_manager.dialog_data["action"] = button.widget_id
        await dialog_manager.next()

    @staticmethod
    async def username(message: Message, widget, dialog_manager: DialogManager) -> None:
        dialog_manager.dialog_data["username"] = message.text
        dialog_manager.dialog_data.pop("error", None)
        await delete_message(message)
        dialog_manager.show_mode = ShowMode.EDIT
        await dialog_manager.next()

    @staticmethod
    async def password(message: Message, widget, dialog_manager: DialogManager) -> None:
        password = message.text
        await delete_message(message)

        data = dialog_manager.dialog_data
        username = data.pop("username")
        action = (
            auth_service.register
            if data["action"] == "register"
            else auth_service.login
        )
        try:
            tokens = await action(username, password, message.from_user.id)
        except AuthError as error:
            data["error"] = html.escape(str(error))
            dialog_manager.show_mode = ShowMode.EDIT
            await dialog_manager.switch_to(AuthState.username)
            return

        state: FSMContext = dialog_manager.middleware_data["state"]
        await state.update_data(access=tokens["access"], refresh=tokens["refresh"])
        prompt_id = dialog_manager.current_stack().last_message_id
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await dialog_manager.done()
        await delete_prompt(message, prompt_id)
        await message.answer(f"You are logged in\n{COMMANDS}")
