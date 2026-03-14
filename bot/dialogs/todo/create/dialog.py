from aiogram_dialog import Dialog

from .windows import (
    body_window,
    category_window,
    confirm_window,
    deadline_window,
    title_window,
)

create_dialog = Dialog(
    title_window, body_window, category_window, deadline_window, confirm_window,
)
