from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart

from keyboards.reply import main
from data import texts


router = Router()


@router.message(CommandStart())
async def start_bot(message: Message):
    await message.answer(texts.txt_main, 
                         reply_markup=main)
    

@router.message(Command('id'))
async def id(message: Message):
    print(f"{message.chat.id}, {message.from_user.first_name}")
    await message.answer(text=str(message.chat.id), 
                         reply_markup=main)
