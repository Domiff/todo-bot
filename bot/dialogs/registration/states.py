from aiogram.filters.state import State, StatesGroup


class RegistrationState(StatesGroup):
    confirm = State()
