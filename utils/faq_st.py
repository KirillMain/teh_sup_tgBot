from aiogram.fsm.state import StatesGroup, State


class FaqState(StatesGroup):
    main = State()
    answer = State()
    back = State()