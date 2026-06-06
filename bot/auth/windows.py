from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from .handlers import RegistrationHandlers
from .states import RegistrationState


class RegistrationWindows:
    confirm = Window(
        Const("Hello! Register in system?"),
        Button(Const("Confirm"), id="confirm", on_click=RegistrationHandlers.confirm),
        state=RegistrationState.confirm,
    )
