from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Column, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.todo.getters import tasks_getter
from bot.dialogs.todo.update.handlers import cancel_handler

from .handlers import choose_task_handler, confirm_handler
from .states import DeleteStates

choose_task_window = Window(
    Format("Select a task or cancel deleting:"),
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
    state=DeleteStates.choose_task,
    getter=tasks_getter,
)


confirm_window = Window(
    Const("Confirm deleting task:"),
    Button(Const("Confirm"), id="confirm_update", on_click=confirm_handler),
    state=DeleteStates.confirm,
)
