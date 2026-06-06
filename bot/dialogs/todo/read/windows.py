from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from .handlers import get_tasks_handler
from .states import ReadState

read_window = Window(
    Const("Show tasks"),
    Button(Const("Show tasks"), id="tasks", on_click=get_tasks_handler),
    state=ReadState.read,
)
