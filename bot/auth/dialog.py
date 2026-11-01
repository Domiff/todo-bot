from aiogram_dialog import Dialog

from .windows import AuthWindows

auth_dialog = Dialog(AuthWindows.choose, AuthWindows.username, AuthWindows.password)
