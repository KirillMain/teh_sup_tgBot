from aiogram.utils.keyboard import ReplyKeyboardBuilder


def faq_builder(count: int):

    builder = ReplyKeyboardBuilder()

    for i in range(count):
        builder.button(text=str(i+1))

    row = []
    while count > 0:
        if count >= 4:
            row.append(4)
            count -= 4
        else:
            row.append(count)
            count = 0
    builder.button(text="⬅Назад")

    builder.adjust(*row, 1)
    return builder.as_markup(resize_keyboard=True)


def appeal_builder(txt: str | list, row: list=[1]):
    if isinstance(txt, str):
        txt = [txt]

    builder = ReplyKeyboardBuilder()
    [builder.button(text=el) for el in txt]

    builder.adjust(*row)
    return builder.as_markup(resize_keyboard=True)