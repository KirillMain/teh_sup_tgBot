from aiogram.fsm.state import StatesGroup, State


class AdmFaqState(StatesGroup):
    main = State()
    choise = State()
    remove_choise = State()
    remove_confirm = State()
    add_que = State()
    add_ans = State()
    add_img = State()
    add_confirm = State()