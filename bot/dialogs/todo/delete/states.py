from aiogram.fsm.state import State, StatesGroup


class DeleteStates(StatesGroup):
    choose_task = State()
    confirm = State()
