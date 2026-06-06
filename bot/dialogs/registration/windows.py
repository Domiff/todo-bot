from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from .handlers import confirm_registration
from .states import RegistrationState

confirm_window = Window(
    Const("Hello! Register in system?"),
    Button(Const("Confirm"), id="confirm", on_click=confirm_registration),
    state=RegistrationState.confirm,
)
