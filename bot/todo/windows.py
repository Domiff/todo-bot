from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Column, Select
from aiogram_dialog.widgets.text import Const, Format

from .handlers import CreateHandlers, DeleteHandlers, ReadHandlers, UpdateHandlers
from .states import CreateStates, DeleteStates, ReadState, UpdateState


class CreateWindows:
    title = Window(
        Const("Enter title: "),
        TextInput(id="title", on_success=CreateHandlers.title),
        state=CreateStates.title,
    )
    body = Window(
        Const("Enter body: "),
        TextInput(id="body", on_success=CreateHandlers.body),
        state=CreateStates.body,
    )
    deadline = Window(
        Const("Enter deadline in format DD.MM.YYYY HH:MM: "),
        TextInput(id="deadline", on_success=CreateHandlers.deadline),
        state=CreateStates.deadline,
    )
    priority = Window(
        Const("Choose priority: "),
        Button(Const("Low"), id="low", on_click=CreateHandlers.priority),
        Button(Const("Middle"), id="middle", on_click=CreateHandlers.priority),
        Button(Const("High"), id="high", on_click=CreateHandlers.priority),
        state=CreateStates.priority,
    )
    category = Window(
        Const("Choose category: "),
        Column(
            Select(
                text=Format("{item[name]}"),
                id="category_select",
                items="categories",
                item_id_getter=lambda item: item["slug"],
                on_click=CreateHandlers.category,
            ),
        ),
        Button(
            Const("No category"),
            id="no_category",
            on_click=CreateHandlers.skip_category,
        ),
        state=CreateStates.category,
        getter=ReadHandlers.categories_getter,
    )
    confirm = Window(
        Const("Confirm create task"),
        Button(Const("Confirm"), id="confirm_tasks", on_click=CreateHandlers.confirm),
        state=CreateStates.confirm,
    )


class ReadWindows:
    read = Window(
        Const("Show tasks"),
        Button(Const("Show tasks"), id="tasks", on_click=ReadHandlers.get_tasks),
        state=ReadState.read,
    )


class UpdateWindows:
    choose_task = Window(
        Format("Select a task or cancel updating:"),
        Column(
            Select(
                text=Format("{item[title]}"),
                id="task_select",
                items="tasks",
                item_id_getter=lambda item: str(item["pk"]),
                on_click=UpdateHandlers.choose_task,
            ),
        ),
        Button(Const("Cancel"), id="cancel", on_click=UpdateHandlers.cancel),
        state=UpdateState.choose_task,
        getter=ReadHandlers.tasks_getter,
    )
    choose_field = Window(
        Const("Choose field:"),
        Button(Const("title"), id="task_title", on_click=UpdateHandlers.choose_field),
        Button(Const("body"), id="task_body", on_click=UpdateHandlers.choose_field),
        Button(
            Const("deadline"), id="task_deadline", on_click=UpdateHandlers.choose_field
        ),
        Button(
            Const("priority"), id="task_priority", on_click=UpdateHandlers.choose_field
        ),
        Button(
            Const("category"), id="task_category", on_click=UpdateHandlers.choose_field
        ),
        Button(Const("status"), id="task_status", on_click=UpdateHandlers.choose_field),
        state=UpdateState.choose_field,
    )
    title = Window(
        Const("Enter a new title or confirm to update the data:"),
        TextInput(id="task_title", on_success=UpdateHandlers.edit_title),
        Button(
            Const("Confirm updates"),
            id="confirm_title",
            on_click=UpdateHandlers.confirm,
        ),
        state=UpdateState.title,
    )
    body = Window(
        Const("Enter a new body or confirm to update the data:"),
        TextInput(id="task_body", on_success=UpdateHandlers.edit_body),
        Button(
            Const("Confirm updates"), id="confirm_body", on_click=UpdateHandlers.confirm
        ),
        state=UpdateState.body,
    )
    deadline = Window(
        Const(
            "Enter a new deadline in format DD.MM.YYYY HH:MM or confirm to update the data:"
        ),
        TextInput(id="task_deadline", on_success=UpdateHandlers.edit_deadline),
        Button(
            Const("Confirm updates"),
            id="confirm_deadline",
            on_click=UpdateHandlers.confirm,
        ),
        state=UpdateState.deadline,
    )
    priority = Window(
        Const("Choose a new priority or confirm to update the data:"),
        Button(Const("Low"), id="low", on_click=UpdateHandlers.edit_priority),
        Button(Const("Middle"), id="middle", on_click=UpdateHandlers.edit_priority),
        Button(Const("High"), id="high", on_click=UpdateHandlers.edit_priority),
        Button(
            Const("Confirm updates"),
            id="confirm_priority",
            on_click=UpdateHandlers.confirm,
        ),
        state=UpdateState.priority,
    )
    category = Window(
        Const("Choose a new category or confirm to update the data:"),
        Column(
            Select(
                text=Format("{item[name]}"),
                id="category_select",
                items="categories",
                item_id_getter=lambda item: item["slug"],
                on_click=UpdateHandlers.edit_category,
            ),
        ),
        Button(
            Const("Confirm updates"),
            id="confirm_category",
            on_click=UpdateHandlers.confirm,
        ),
        state=UpdateState.category,
        getter=ReadHandlers.categories_getter,
    )
    confirm = Window(
        Const("Confirm updating task:"),
        Button(Const("Confirm"), id="confirm_update", on_click=UpdateHandlers.confirm),
        state=UpdateState.confirm,
    )
    status = Window(
        Const("Choose a new status:"),
        Button(Const("Done"), id="done", on_click=UpdateHandlers.edit_status),
        Button(
            Const("In progress"), id="in_progress", on_click=UpdateHandlers.edit_status
        ),
        Button(Const("Cancel"), id="cancel", on_click=UpdateHandlers.cancel),
        state=UpdateState.status,
    )


class DeleteWindows:
    choose_task = Window(
        Format("Select a task or cancel deleting:"),
        Column(
            Select(
                text=Format("{item[title]}"),
                id="task_select",
                items="tasks",
                item_id_getter=lambda item: str(item["pk"]),
                on_click=DeleteHandlers.choose_task,
            ),
        ),
        Button(Const("Cancel"), id="cancel", on_click=UpdateHandlers.cancel),
        state=DeleteStates.choose_task,
        getter=ReadHandlers.tasks_getter,
    )
    confirm = Window(
        Const("Confirm deleting task:"),
        Button(Const("Confirm"), id="confirm_delete", on_click=DeleteHandlers.confirm),
        state=DeleteStates.confirm,
    )
