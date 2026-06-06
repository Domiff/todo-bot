from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from .handlers import (
    body_handler,
    confirm_create_handler,
    deadline_handler,
    primary_handler,
    secondary_handler,
    title_handler,
)
from .states import CreateStates

title_window = Window(
    Const("Enter title: "),
    TextInput(id="title", on_success=title_handler),
    state=CreateStates.title,
)

body_window = Window(
    Const("Enter body: "),
    TextInput(id="body", on_success=body_handler),
    state=CreateStates.body,
)

deadline_window = Window(
    Const("Enter deadline in format DD.MM.YYYY HH:MM: "),
    TextInput(id="deadline", on_success=deadline_handler),
    state=CreateStates.deadline,
)

category_window = Window(
    Const("Enter category: "),
    Button(Const("Primary"), id="primary", on_click=primary_handler),
    Button(Const("Secondary"), id="secondary", on_click=secondary_handler),
    state=CreateStates.category,
)

confirm_window = Window(
    Const("Confirm create task"),
    Button(Const("Confirm"), id="confirm_tasks", on_click=confirm_create_handler),
    state=CreateStates.confirm,
)
