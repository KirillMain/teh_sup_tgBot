from aiogram.fsm.state import StatesGroup, State


class UsAppState(StatesGroup):
    main = State()
    appeal = State()
    answer = State()