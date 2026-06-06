from aiogram_dialog import Dialog

from .windows import CreateWindows, DeleteWindows, ReadWindows, UpdateWindows

create_dialog = Dialog(
    CreateWindows.title,
    CreateWindows.body,
    CreateWindows.category,
    CreateWindows.deadline,
    CreateWindows.confirm,
)

read_dialog = Dialog(ReadWindows.read)

update_dialog = Dialog(
    UpdateWindows.choose_task,
    UpdateWindows.choose_field,
    UpdateWindows.title,
    UpdateWindows.body,
    UpdateWindows.deadline,
    UpdateWindows.confirm,
)

delete_dialog = Dialog(
    DeleteWindows.choose_task,
    DeleteWindows.confirm,
)
