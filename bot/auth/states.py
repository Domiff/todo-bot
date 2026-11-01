from aiogram.filters.state import State, StatesGroup


class AuthState(StatesGroup):
    choose = State()
    username = State()
    password = State()
