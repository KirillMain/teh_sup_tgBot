from aiogram.fsm.state import StatesGroup, State


class AppealState(StatesGroup):
    type = State()
    content = State()
    img = State()
    res = State()
    last = State()