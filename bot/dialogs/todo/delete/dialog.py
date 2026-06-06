from aiogram_dialog import Dialog

from .windows import choose_task_window, confirm_window

delete_dialog = Dialog(choose_task_window, confirm_window)
