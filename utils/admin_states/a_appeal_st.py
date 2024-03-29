from aiogram.fsm.state import StatesGroup, State


class AdmAppState(StatesGroup):
    main = State()
    choise = State()
    num_of_appeal = State()
    random_appeal = State()
    answer = State()
    img = State()
    res = State()