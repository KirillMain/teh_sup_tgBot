from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.usappeals_st import UsAppState
from data import database as db 
from keyboards import builder, reply
from data import texts


router = Router()


@router.message(F.text.lower().in_(["мои обращения"]))
async def form_usersappeals(message: Message, state: FSMContext):
    await state.set_state(UsAppState.main)
    await form_usersappeals_main(message, state)


@router.message(UsAppState.main)
async def form_usersappeals_main(message: Message, state: FSMContext):
    u_id = message.from_user.id
    data = await db.db_appeal_get(u_id)
    # id, date, type, content, img, answer

    if data != []:
        txt = ""
        for i in range(len(data)):
            txt += f"Обращение №{i+1}\n{data[i][3]}: {data[i][4][:10]}..?\n\n"
        txt += "Нажмите на кнопку с номером обращения"

        await state.update_data(main=data)
        await state.set_state(UsAppState.appeal)
        await message.answer(txt, reply_markup=builder.faq_builder(len(data)))
    
    else: 
        await state.clear()
        await message.answer("У Вас пока нету обращений")


@router.message(UsAppState.appeal)
async def form_usersappeals_appeal(message: Message, state: FSMContext):
    data_state = await state.get_data()
    data = data_state['main']
    # id, date, type, content, img, answer

    if message.text.isdigit() and int(message.text)<=len(data):
        num = int(message.text)
        txt = texts.txt_appeal(data[num-1])

        await state.update_data(appeal=num-1)
        await state.set_state(UsAppState.answer)
        if data[num-1][6] == None:
            txt += "\n\n 🔴 Ответа нет"
            if data[num-1][5] == None:
                await message.answer(txt,
                                    reply_markup=builder.appeal_builder(txt=["⬅Назад"]))
            else: 
                await message.answer_photo(data[num-1][5], txt,
                                           reply_markup=builder.appeal_builder(txt=["⬅Назад"]))
        else:
            txt += "\n\n 🟢 Ответ дан"
            if data[num-1][5] == None:
                await message.answer(txt,
                                    reply_markup=builder.appeal_builder(["Посмотреть ответ", "⬅Назад"], [1, 1]))
            else:
                await message.answer_photo(data[num-1][5], txt,
                                    reply_markup=builder.appeal_builder(["Посмотреть ответ", "⬅Назад"], [1, 1]))
                
    else:
        await state.clear()
        await message.answer(texts.txt_main, 
                             reply_markup=reply.main)


@router.message(UsAppState.answer)
async def form_usersappeals_answer(message: Message, state: FSMContext):
    if message.text.lower() == "посмотреть ответ":
        data_state = await state.get_data()
        data = data_state['main']
        # id, date, type, content, img, answer, answer_img
        num = data_state["appeal"]

        txt = f"Ответ администратора:\n{data[num][6]}"

        if data[num][7] == None:
            await message.answer(txt, 
                                reply_markup=builder.appeal_builder(txt=["⬅Назад"]))
        else: 
            await message.answer_photo(data[num][7], txt, 
                                reply_markup=builder.appeal_builder(txt=["⬅Назад"]))

    
    else:
        await state.set_state(UsAppState.main)
        await form_usersappeals_main(message, state)
