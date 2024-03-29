from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import a_main
from filters.is_admin import IsAdmin
from data import database as db
from keyboards import builder
from utils.admin_states.a_faq_st import AdmFaqState
from data import texts

from config_reader import config


router = Router()
router.message.filter(
    IsAdmin(config.admin_ids)
)


@router.message(F.text.lower().in_(["изменить faq"]), IsAdmin)
async def a_form_faq(message: Message, state: FSMContext):
    await state.set_state(AdmFaqState.main)
    await a_form_faq_main(message, state)
    

@router.message(AdmFaqState.main)
async def a_form_faq_main(message: Message, state: FSMContext):
    data =  await db.db_faq_count()

    if len(data) == 0:
        txt = "Список FAQ пока пуст"
        await state.update_data(main=data)
        await state.set_state(AdmFaqState.choise)
        await message.answer(txt,
                            reply_markup=builder.appeal_builder(["Добавить", "⬅Назад"], [1, 1]))
    else: 
        txt = "Список FAQ"
        for i in range(len(data)):
            txt += f"\n\n№{i+1} - {data[i][1]}"

        await state.update_data(main=data)
        await state.set_state(AdmFaqState.choise)
        await message.answer(txt,
                            reply_markup=builder.appeal_builder(["Удалить", "Добавить", "⬅Назад"], [2, 1]))
    

@router.message(AdmFaqState.choise)
async def a_form_faq_choise(message: Message, state: FSMContext):
    if message.text.lower() == "удалить":
        data =  await state.get_data()
        data = data["main"]

        txt = "Список FAQ"
        for i in range(len(data)):
            txt += f"\n\n№{i+1} - {data[i][1]}"

        await state.set_state(AdmFaqState.remove_choise)
        await message.answer(txt,
                             reply_markup=builder.faq_builder(len(data)))
    
    elif message.text.lower() == 'добавить':
        await state.set_state(AdmFaqState.add_que)
        await message.answer("Напишите вопрос",
                             reply_markup=builder.appeal_builder(txt="Отмена"))

    else:
        await state.clear()
        await message.answer(texts.txt_a_main, 
                             reply_markup=a_main)


# ------------------------------ REMOVE ------------------------------
@router.message(AdmFaqState.remove_choise)
async def a_form_faq_removeChoise(message: Message, state: FSMContext):
    data =  await state.get_data()
    data = data["main"]

    if message.text.isdigit() and int(message.text) <= len(data):
        num = data[int(message.text)-1][0]
        await state.update_data(remove_choise=num)
        await state.set_state(AdmFaqState.remove_confirm)
        await message.answer("Вы действительно хотите удалить данный вопрос?",
                             reply_markup=builder.appeal_builder(['Нет', 'Да'], [2]))
    
    elif message.text == "⬅Назад":
        await a_form_faq(message, state)


@router.message(AdmFaqState.remove_confirm)
async def a_form_faq_removeConfirm(message: Message, state: FSMContext, bot: Bot):
    if message.text.lower() == "да":
        data = await state.get_data()
        await db.a_db_faq_remove(data['remove_choise'])
        await bot.send_message(message.from_user.id, "Вопрос успешно удален")

    await a_form_faq(message, state)


# ------------------------------ ADD ------------------------------
@router.message(AdmFaqState.add_que)
async def a_form_faq_addQue(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await a_form_faq(message, state)

    elif message.text[-1] != "?":
        await message.answer("Добавьте вопрос в конце (Например: Что есть бытие?)")

    else:
        await state.update_data(add_que=message.text)
        await state.set_state(AdmFaqState.add_ans)
        await message.answer("Напишите ответ на вопрос", 
                             reply_markup=builder.appeal_builder("Отмена"))


@router.message(AdmFaqState.add_ans)
async def a_form_faq_addAns(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await a_form_faq(message, state)

    else: 
        await state.update_data(add_ans=message.text)
        await state.set_state(AdmFaqState.add_img)
        await message.answer("Добавьте изображение к ответу", 
                            reply_markup=builder.appeal_builder(['Без изображения', 'Отмена'], [1, 1]))


@router.message(AdmFaqState.add_img, F.photo)
async def a_form_faq_addImg(message: Message, state: FSMContext):
    img_id = message.photo[-1].file_id
    data = await state.get_data()
    txt = f"Вопрос: {data['add_que']}\nОтвет:\n{data['add_ans']}\n\nВы действительно хотите добавить этот вопрос к списку FAQ"

    await state.update_data(add_img=img_id)
    await state.set_state(AdmFaqState.add_confirm)
    await message.answer_photo(img_id, txt, 
                               reply_markup=builder.appeal_builder(['Нет', 'Да'], [2]))
    

@router.message(AdmFaqState.add_img, ~F.photo)
async def a_form_faq_addImg(message: Message, state: FSMContext):
    if message.text.lower() == 'без изображения':
        data = await state.get_data()
        txt = f"Вопрос: {data['add_que']}\nОтвет:\n{data['add_ans']}\n\nВы действительно хотите добавить этот вопрос к списку FAQ"

        await state.update_data(add_img=None)
        await state.set_state(AdmFaqState.add_confirm)
        await message.answer(txt, 
                            reply_markup=builder.appeal_builder(['Нет', 'Да'], [2]))
    else: 
        await a_form_faq(message, state)



@router.message(AdmFaqState.add_confirm)
async def a_form_faq_addConfirm(message: Message, state: FSMContext, bot: Bot):
    if message.text.lower() == "да":
        data = await state.get_data()
        await db.a_db_faq_add(data['add_que'], data['add_ans'], data['add_img'])
        await state.clear()
        await state.set_state(AdmFaqState.main)
        await bot.send_message(message.from_user.id, "Вопрос-ответ успешно добавлен в список FAQ")
        await a_form_faq_main(message, state)
    
    else:
        await a_form_faq(message, state)


async def a_form_return(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AdmFaqState.main)
    await a_form_faq_main(message, state)