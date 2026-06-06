from aiogram.fsm.state import State, StatesGroup


class CreateStates(StatesGroup):
    title = State()
    body = State()
    deadline = State()
    category = State()
    confirm = State()


class ReadState(StatesGroup):
    read = State()


class UpdateState(StatesGroup):
    choose_task = State()
    choose_field = State()
    title = State()
    body = State()
    deadline = State()
    category = State()
    confirm = State()


class DeleteStates(StatesGroup):
    choose_task = State()
    confirm = State()
