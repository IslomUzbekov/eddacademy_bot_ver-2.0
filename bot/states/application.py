from aiogram.fsm.state import State, StatesGroup


class ApplicationStates(StatesGroup):
    full_name = State()
    phone = State()
    age = State()
    course = State()
    confirm = State()


class CourseStates(StatesGroup):
    page = State()


class ReviewStates(StatesGroup):
    institution_text = State()
    course_score = State()
    course_text = State()
