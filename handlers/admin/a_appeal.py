from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import AiogramError

from keyboards.reply import a_main
from filters.is_admin import IsAdmin
from data import database as db
from keyboards import builder
from utils.admin_states.a_appeal_st import AdmAppState
from data import texts

from config_reader import config


router = Router()
router.message.filter(
    IsAdmin(config.admin_ids)
)


@router.message(F.text.lower().in_(['ответить на обращение']))
async def a_appeal(message: Message, state: FSMContext):
    await state.set_state(AdmAppState.main)
    await a_appeal_main(message, state)


@router.message(AdmAppState.main)
async def a_appeal_main(message: Message, state: FSMContext):
    await state.set_state(AdmAppState.choise)
    await message.answer("Какое обращение вы хотите выбрать для ответа?",
                         reply_markup=builder.appeal_builder(["Случайное", "По номеру", "Отмена"], [2, 1]))


# сокращение функции
async def send_messages(message, state, bot, appeal):
    txt = texts.txt_appeal(appeal=appeal)
    await state.update_data(choise=appeal)
    await state.set_state(AdmAppState.answer)

    if appeal[5] == None:
        await message.answer(txt,
                             reply_markup=builder.appeal_builder('Отмена'))
    else: 
        await message.answer_photo(appeal[5], txt,
                                   reply_markup=builder.appeal_builder('Отмена'))
    await bot.send_message(message.from_user.id, "Дайте ответ на данное обращение")


@router.message(AdmAppState.choise)
async def a_appeal_choise(message: Message, state: FSMContext, bot: Bot):
    if message.text.lower() == "случайное":
        data = await db.a_db_appeal_get_no_id()
        appeal = None
        for el in data:
            if el[6] == None:
                appeal = el

        if appeal == None:
            await message.answer("Обращений без ответа нет")
        else: 
            await send_messages(message, state, bot, appeal)
            
    elif message.text.lower() == "по номеру":
        await state.set_state(AdmAppState.num_of_appeal)
        await message.answer("Введите номер обращения",
                             reply_markup=builder.appeal_builder("Отмена"))
        
    else:
        await state.clear()
        await message.answer(texts.txt_a_main, 
                             reply_markup=a_main)
        

@router.message(AdmAppState.num_of_appeal)
async def a_appeal_numOfAppeal(message: Message, state: FSMContext, bot: Bot):
    if message.text.isdigit():
        appeal = await db.a_db_appeal_get_id(int(message.text))
        
        if appeal == None:
            return await message.answer("Такого обращения не существует")
        
        if appeal[-2] == None:
            await send_messages(message, state, bot, appeal)
        else: 
            await message.answer("Ответ на это обращение уже дан")

    elif message.text.lower() == 'отмена':
        await state.clear()
        await state.set_state(AdmAppState.main)
        await a_appeal_main(message, state)

    else:
        await message.answer("Введите число!")


@router.message(AdmAppState.answer)
async def a_appeal_answer(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.clear()
        await state.set_state(AdmAppState.main)
        await a_appeal_main(message, state)

    else: 
        await state.update_data(answer=message.text)
        await state.set_state(AdmAppState.img)
        await message.answer("Пришлите к вашему ответу изображение", 
                             reply_markup=builder.appeal_builder(["Без изображения", "Отмена"], [1, 1]))


@router.message(AdmAppState.img, F.photo)
async def a_appeal_img(message: Message, state: FSMContext):
    img_id = message.photo[-1].file_id
    await state.update_data(img=img_id)
    await a_appeal_send_res(message, state, True)
    

@router.message(AdmAppState.img, ~F.photo)
async def a_appeal_no_photo(message: Message, state: FSMContext):
    if message.text.lower() == 'без изображения':
        await state.update_data(img=None)
        await a_appeal_send_res(message, state, False)

    else: 
        await state.clear()
        await state.set_state(AdmAppState.main)
        await a_appeal_main(message, state)


async def a_appeal_send_res(message: Message, state: FSMContext, photo: bool):
    data = await state.get_data()
    txt = texts.txt_appeal(data['choise'])
    txt2 = f"Ваш ответ: {data['answer']}\n\n" \
           f"Вы действительно хотите ответить на обращение?"
    await state.set_state(AdmAppState.res)
    
    if photo:
        if data['choise'][5] == None:
            await message.answer(txt)
            await message.answer_photo(data['img'], txt2,
                                       reply_markup=builder.appeal_builder(['Нет', "Да"], [2]))
        else: 
            await message.answer_photo(data['choise'][5], txt)
            await message.answer_photo(data['img'], txt2,
                                       reply_markup=builder.appeal_builder(['Нет', "Да"], [2]))
            
    else: 
        if data['choise'][5] == None:
            await message.answer(txt)
            await message.answer(txt2,
                                 reply_markup=builder.appeal_builder(['Нет', "Да"], [2]))
        else: 
            await message.answer_photo(data['choise'][5], txt)
            await message.answer(txt2,
                                 reply_markup=builder.appeal_builder(['Нет', "Да"], [2]))

        
@router.message(AdmAppState.res)
async def a_appeal_res(message: Message, state: FSMContext, bot: Bot):
    if message.text.lower() == "да":
        data = await state.get_data()
        appeal_id = data['choise'][0]
        answer = data['answer']
        img = data['img']

        await db.a_db_appeal_update(appeal_id, answer, img)
        await message.answer("Ответ успешно добавлен")

        # УВЕДОМЛЕНИЕ
        user_id = data['choise'][1]
        await bot.send_message(user_id, f"На Ваше обращение №{appeal_id} дан ответ!")
        # УВЕДОМЛЕНИЕ
    
    await state.clear()
    await state.set_state(AdmAppState.main)
    await a_appeal_main(message, state)
