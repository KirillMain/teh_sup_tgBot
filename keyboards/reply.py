from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Написать обращение"),
            KeyboardButton(text="Мои обращения")
        ],
        [
            KeyboardButton(text="Часто задаваемые вопросы")
        ]
    ],
    resize_keyboard=True
)


a_main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ответить на обращение"),
            KeyboardButton(text="Изменить FAQ")
        ],
        [
            KeyboardButton(text="Вернуться в обычный аккаунт")
        ]
    ],
    resize_keyboard=True
)


rmk = ReplyKeyboardRemove()