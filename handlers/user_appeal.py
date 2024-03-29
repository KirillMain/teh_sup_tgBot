from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.appeal_st import AppealState
from keyboards.builder import appeal_builder
from keyboards.reply import main
from data import texts
from data import database as db
from config_reader import config

from datetime import datetime


router = Router()


@router.message(F.text.lower().in_(["написать обращение", "обращение"]))
async def form_appeal(message: Message, state: FSMContext):
    await state.set_state(AppealState.type)
    await message.answer("Выберите тип обращения", 
                         reply_markup=appeal_builder(["Жалоба", "Вопрос", "Отмена"], [2, 1]))
    

@router.message(AppealState.type)
async def form_appeal_type(message: Message, state: FSMContext):
    if message.text.lower() in ["жалоба", "вопрос"]:
        await state.update_data(type=message.text)
        await state.set_state(AppealState.content)
        await message.answer("Опишите вашу проблему",
                            reply_markup=appeal_builder(["Отмена"]))
        
    else:
        form_appeal_last(message, state)


@router.message(AppealState.content)
async def form_appeal_text(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        form_appeal_last(message, state)

    elif len(message.text) > 10:
        await state.update_data(content=message.text)
        await state.set_state(AppealState.img)
        await message.answer("Пришлите изображение",
                            reply_markup=appeal_builder(["Без изображения", "Отмена"], [1, 1]))
    else: 
        await message.answer("Опишите проблему поподробнее")
    

@router.message(AppealState.img, F.photo)
async def form_appeal_img_y(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()
    await state.update_data(img=photo_file_id)
    await state.set_state(AppealState.res)

    txt = texts.txt_new_appeal(data)
    await message.answer_photo(photo_file_id, txt, 
                               reply_markup=appeal_builder(["Нет", "Да"], [2]))
        

@router.message(AppealState.img, ~F.photo)
async def form_appeal_img_n(message: Message, state: FSMContext):
    if message.text.lower() == "без изображения":
        data = await state.get_data()
        await state.set_state(AppealState.res)  

        txt = texts.txt_new_appeal(data)
        await message.answer(txt,
                             reply_markup=appeal_builder(["Нет", "Да"], [2]))
    else:
        form_appeal_last(message, state)


@router.message(AppealState.res)
async def form_appeal_res(message: Message, state: FSMContext, bot: Bot):
    if message.text.lower() == "да":
        # db update
        data = await state.get_data()
        data['date'] = datetime.now().date()
        data['user_id'] = message.from_user.id
        if 'img' not in data.keys():
            data['img'] = None
        await db.db_appeal_new(data)
        # db close

        # УВЕДОМЛЕНИЕ
        data_for_alarm = await db.a_db_appeal_get_no_id()
        latest = data_for_alarm[-1]
        if data['img'] == None:
            await bot.send_message(config.chat_id, 
                                   texts.txt_appeal(latest))
        else:
            await bot.send_photo(int(config.chat_id),
                                 data['img'],
                                 caption=texts.txt_appeal(latest))
        # УВЕДОМЛЕНИЕ

        await state.set_state(AppealState.last)  
        await message.answer("Обращение успешно отправлено", 
                             reply_markup=appeal_builder("В главное меню"))     
    else:
        form_appeal_last(message, state)


@router.message(AppealState.last)
async def form_appeal_last(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.txt_main,
                         reply_markup=main)



    



    