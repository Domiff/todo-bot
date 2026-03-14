from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Column, Select
from aiogram_dialog.widgets.text import Const, Format

from ..getters import tasks_getter
from .handlers import (
    cancel_handler,
    choose_filed_handler,
    choose_task_handler,
    confirm_handler,
    edit_body_handler,
    edit_category_handler,
    edit_deadline_handler,
    edit_title_handler,
)
from .states import UpdateState

choose_task_window = Window(
    Format("Select a task or cancel updating:"),
    Column(
        Select(
            text=Format("{item[title]}"),
            id="task_select",
            items="tasks",
            item_id_getter=lambda item: str(item["pk"]),
            on_click=choose_task_handler,
        ),
    ),
    Button(Const("Cancel"), id="cancel", on_click=cancel_handler),
    state=UpdateState.choose_task,
    getter=tasks_getter,
)

choose_field_window = Window(
    Const("Choose field:"),
    Button(Const("title"), id="task_title", on_click=choose_filed_handler),
    Button(Const("body"), id="task_body", on_click=choose_filed_handler),
    Button(Const("deadline"), id="task_deadline", on_click=choose_filed_handler),
    state=UpdateState.choose_field,
)


title_window = Window(
    Const("Enter a new title or confirm to update the data:"),
    TextInput(id="task_title", on_success=edit_title_handler),
    Button(Const("Confirm updates"), id="confirm_title", on_click=confirm_handler),
    state=UpdateState.title,
)


body_window = Window(
    Const("Enter a new body or confirm to update the data:"),
    TextInput(id="task_body", on_success=edit_body_handler),
    Button(Const("Confirm updates"), id="confirm_body", on_click=confirm_handler),
    state=UpdateState.body,
)


deadline_window = Window(
    Const(
        "Enter a new deadline in format DD.MM.YYYY HH:MM or confirm to update the data:",
    ),
    TextInput(id="task_deadline", on_success=edit_deadline_handler),
    Button(Const("Confirm updates"), id="confirm_deadline", on_click=confirm_handler),
    state=UpdateState.deadline,
)


category_window = Window(
    Const("Choose category:"),
    Button(Const("Primary"), id="primary", on_click=edit_category_handler),
    Button(Const("Secondary"), id="secondary", on_click=edit_category_handler),
    Button(Const("Confirm updates"), id="confirm_title", on_click=confirm_handler),
    state=UpdateState.category,
)


confirm_window = Window(
    Const("Confirm updating task:"),
    Button(Const("Confirm"), id="confirm_update", on_click=confirm_handler),
    state=UpdateState.confirm,
)
