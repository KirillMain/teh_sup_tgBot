from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import reply
from filters.is_admin import IsAdmin
from data import texts

from config_reader import config


router = Router()
router.message.filter(
    IsAdmin(config.admin_ids)
)


@router.message(Command("apanel"), IsAdmin)
async def admin_panel(message: Message):
    await message.answer("Вы вошли в админ панель", 
                         reply_markup=reply.a_main)
    

@router.message(F.text.lower().in_(["вернуться в обычный аккаунт"]))
async def to_user_acc(message: Message):
    await message.answer("Вы вернулись в обычный аккаунт")
    await message.answer(texts.txt_main, 
                         reply_markup=reply.main)
    