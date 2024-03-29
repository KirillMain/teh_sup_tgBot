from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.faq_st import FaqState
from data import database as db 
from keyboards import builder, reply
from data import texts


router = Router()


# FAQ список
@router.message(F.text.lower().in_(["часто задаваемые вопросы", "faq"]))
async def form_faq(message: Message, state: FSMContext):
    await state.set_state(FaqState.main)
    await form_faq_main(message, state)
    

@router.message(FaqState.main)
async def form_faq_main(message: Message, state: FSMContext):
    data = await db.db_faq_count()

    if data == None:
        txt = "Пока что нету часто задаваемых вопросов"
        await state.clear()
    else:
        count = len(data)
        txt = ""
        for i in range(count):
            txt += f"\n\n№{i+1}: " + data[i][1]
        txt += "\n\nНажмите на номер вопроса, ответ на который хотите посмотреть."
        await state.update_data(main=data)
    
    await state.set_state(FaqState.answer)
    await message.answer(f"Список FAQ{txt}",
                         reply_markup=builder.faq_builder(count))
    

@router.message(FaqState.answer)
async def form_faq_answer(message: Message, state: FSMContext):
    if message.text.isdigit():
        main_data = await state.get_data()
        data = main_data['main']
        count = len(data)
        num  = int(message.text)
        if num <= count:
            txt = f"{data[num-1][1]}\n\nОтвет: {data[num-1][2]}"
            if data[num-1][3] == None:
                await message.answer(txt)
            else:
                await message.answer_photo(data[num-1][3], txt)
        else: 
            await message.answer("Вопроса с таким номером нету")

    else:
        await state.clear()
        await message.answer(texts.txt_main,
                             reply_markup=reply.main)
