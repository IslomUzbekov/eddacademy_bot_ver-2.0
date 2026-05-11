
from aiogram.fsm.state import State, StatesGroup


class ApplicationStates(StatesGroup):
    full_name = State()
    phone = State()
    age = State()
    course = State()
    confirm = State()
