from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format, Multi

from .handlers import AuthHandlers
from .states import AuthState

not_command = ~F.text.startswith("/")


class AuthWindows:
    choose = Window(
        Const("Hello! Register a new account or log in to an existing one."),
        Button(Const("Register"), id="register", on_click=AuthHandlers.choose),
        Button(Const("Log in"), id="login", on_click=AuthHandlers.choose),
        state=AuthState.choose,
    )
    username = Window(
        Multi(
            Format("{error}", when="error"),
            Const("Enter username (the message will be deleted):"),
        ),
        MessageInput(
            AuthHandlers.username, content_types=ContentType.TEXT, filter=not_command
        ),
        state=AuthState.username,
        getter=AuthHandlers.getter,
    )
    password = Window(
        Const("Enter password (the message will be deleted):"),
        MessageInput(
            AuthHandlers.password, content_types=ContentType.TEXT, filter=not_command
        ),
        state=AuthState.password,
    )
