from aiogram_dialog import DialogManager

from bot.crud import get_tasks


async def tasks_getter(dialog_manager: DialogManager, **kwargs):
    state = dialog_manager.middleware_data["state"]
    tokens = await state.get_data()
    access = tokens["access"]
    refresh = tokens["refresh"]
    tasks = await get_tasks(access, refresh, state)
    return {
        "tasks": tasks,
    }
