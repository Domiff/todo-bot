from aiogram.fsm.state import State, StatesGroup


class CreateStates(StatesGroup):
    title = State()
    body = State()
    deadline = State()
    category = State()
    confirm = State()
