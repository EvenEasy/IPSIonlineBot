import markups, forms, create_bot
from create_bot import bot, db
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from datetime import datetime

admins = (367961212,1835953916)

async def admin(message : types.Message):
    await message.answer("АДМИН ПАНЕЛЬ", reply_markup=markups.admin_markup)

async def open_admin(callback : types.CallbackQuery):
    await callback.message.edit_text(
        "АДМИН ПАНЕЛЬ",
        reply_markup=markups.admin_markup
    )


# ============= CHAGNE TEXT ==================
async def change_text(callback : types.CallbackQuery):
    try: await callback.answer()
    except Exception: pass
    await callback.message.answer("СПИСОК ТЕКСТУ", reply_markup=markups.list_texts())

async def select_text(callback : types.CallbackQuery, state : FSMContext):
    try: await callback.answer()
    except Exception: pass
    key = callback.data.split('_')[-1]
    await forms.AdminForms.change_text.set()
    await state.update_data(key=key)
    await callback.message.answer(f"{db.get_text(key)}\n\n\nВведите новий текст:",reply_markup=types.ReplyKeyboardMarkup([["НАЗАД"]], True))

async def change_text_set(message : types.Message, state : FSMContext):
    data = await state.get_data()
    await state.finish()

    if message.text == "НАЗАД":
        await message.answer("АДМИН ПАНЕЛЬ", reply_markup=markups.admin_markup)
        return
    db.sqlite1('UPDATE Texts SET Text1 = ? WHERE key = ?', (message.text, data.get('key')))
    await message.answer("Текст успешно изменен", reply_markup=types.ReplyKeyboardRemove())

# ================== SEND MESSAGE =====================

async def send_message(callback : types.CallbackQuery):
    try: await callback.answer()
    except Exception: pass
    await forms.AdminForms.select_receiver.set()
    await callback.message.answer("Виберите пользователя:\n\введите мой Username та оберите пользователя")

async def inline_query(query : types.InlineQuery, state : FSMContext):
    item = [
        types.InlineQueryResultArticle(
            id=user_id,
            title=username,
            input_message_content=types.InputTextMessageContent(user_id),
            description=f"{username} | {user_id}"
        ) for user_id, username in db.get_receivers_list(query.query)
    ]
    await query.answer(item, is_personal=True, cache_time=1)

async def chosen_inline(message : types.Message, state : FSMContext):
    await state.update_data(receiver=message.text)
    await forms.AdminForms.send_message.set()
    await message.answer(f"Введите сообщение", reply_markup=types.ReplyKeyboardMarkup([["СКАСУВАТЬ"]],True,True, input_field_placeholder="введіть повідомлення"))

async def send_messages(message : types.Message, state : FSMContext):
    if message.content_type == types.ContentType.TEXT and message.text == "СКАСУВАТЬ":
        await state.finish()
        await message.answer("АДМИН ПАНЕЛЬ", reply_markup=markups.admin_markup)
        return

    data = await state.get_data()
    await bot.send_message(data.get('receiver'), message.text)
    await message.answer("Сообщение было отправлено!", reply_markup=markups.admin_markup)
    await state.finish()

# ================== ADD QUESTION =====================

async def add_question(callback : types.CallbackQuery):
    try: await callback.answer()
    except Exception: pass
    await forms.AdminForms.add_question.set()
    await callback.message.answer("Введите вопрос", reply_markup=types.ReplyKeyboardMarkup([["СКАСУВАТЬ"]], True))

async def add_question1(message : types.Message, state : FSMContext):
    if message.text == "СКАСУВАТЬ":
        await state.finish()
        await message.answer("АДМИН ПАНЕЛЬ", reply_markup=markups.admin_markup)
        return
    await forms.AdminForms.set_type.set()
    await state.update_data(question=message.text)
    await message.answer("Виберите тип вопроса", reply_markup=types.ReplyKeyboardMarkup([['TEXT', 'CONTACT'],['СКАСУВАТь']], True))

async def add_question2(message : types.Message, state : FSMContext):
    if message.text == "СКАСУВАТЬ":
        await state.finish()
        await message.answer("АДМИН ПАНЕЛЬ", reply_markup=markups.admin_markup)
        return
    data = await state.get_data()
    await state.finish()
    db.sqlite1("INSERT INTO Questions VALUES (?, NULL, ?)", (data.get('question'), message.text))
    await message.answer("Вопрос успешно додан", reply_markup=types.ReplyKeyboardRemove())


async def answer_user(callback : types.CallbackQuery, state : FSMContext):
    chat_id = callback.data.split('_')
    reply_id = chat_id[-1]
    chat_id = chat_id[-2]
    try: await callback.answer()
    except Exception: pass
    await forms.AdminForms.answer_support.set()
    await state.update_data(
        chat_id=int(chat_id),
        reply_id=reply_id
    )
    await callback.message.answer(
        f"{callback.message.text}\n\nВведите сообщение",
        reply_markup=types.ReplyKeyboardMarkup([["СКАСУВАТЬ"]], True, input_field_placeholder="введіть повідомлення для цього користувача")
    )

async def answer_user_message(message : types.Message, state : FSMContext):
    if message.text == "СКАСУВАТЬ":
        await state.finish()
        await message.answer("Відповідь скасована", reply_markup=types.ReplyKeyboardRemove())
        return
    data = await state.get_data()
    await state.finish()
    await bot.send_message(
        chat_id=data.get("chat_id"),
        text=message.text,
        reply_to_message_id=data.get("reply_id"),
    )

# ================== EDIT QUESTION =====================

async def select_question(callback : types.CallbackQuery):
    try: await callback.answer()
    except Exception: pass

    await forms.AdminForms.select_question.set()
    await callback.message.answer(
        "Выберите вопрос",
        reply_markup=markups.list_question_markup()
    )

async def select_question1(callback : types.CallbackQuery, state : FSMContext):
    try: await callback.answer()
    except Exception: pass
    await callback.message.delete()

    row_id = callback.data.split('_')[-1]
    await forms.AdminForms.select_option.set()
    await state.update_data(row_id=row_id)
    await callback.message.answer(
        "Выберите действие",
        reply_markup=markups.optinos
    )

#   EDIT TEXT

async def edit_text_question(callback : types.CallbackQuery, state : FSMContext):
    try: await callback.answer()
    except Exception: pass
    
    await forms.AdminForms.select_option_enter_text.set()
    await callback.message.answer("Введите новый текст вопроса:")

async def enter_text_question(message : types.Message, state : FSMContext):
    data = await state.get_data()
    await forms.AdminForms.select_option.set()
    db.sqlite1("UPDATE Questions SET question = ? WHERE rowid = ?", (message.text, data.get('row_id')))
    await message.answer("Вопрос был успешно изменен !", reply_markup=markups.optinos)

#   EDIT TYPE

async def edit_type_answer(callback : types.CallbackQuery, state : FSMContext):
    try: await callback.answer()
    except Exception: pass
    
    await forms.AdminForms.select_option_enter_type.set()
    await callback.message.answer("Выберите тип ответа:", reply_markup=types.ReplyKeyboardMarkup([['TEXT', 'CONTACT']], True))

async def enter_type_answer(message : types.Message, state : FSMContext):
    data = await state.get_data()
    await forms.AdminForms.select_option.set()
    db.sqlite1("UPDATE Questions SET TYPE = ? WHERE rowid = ?", (message.text, data.get('row_id')))
    await message.answer("Вопрос был успешно изменен !", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(
        "Выберите действие",
        reply_markup=markups.optinos
    )

#   DELETE     

async def delete_question(callback : types.CallbackQuery, state : FSMContext):
    data = await state.get_data()
    db.sqlite(f"DELETE FROM Questions WHERE rowid = {data.get('row_id')}")
    await callback.message.answer("Вопрос был успешно удалён")
    await callback.message.answer("АДМИН ПАНЕЛЬ", reply_markup=markups.admin_markup)

async def exit_optinos(callback : types.CallbackQuery, state : FSMContext):
    await state.finish()
    await callback.message.delete()
    await callback.message.answer("АДМИН ПАНЕЛЬ", reply_markup=markups.admin_markup)

# ================== SQLITE =====================

async def _sqlite(msg : types.Message):
    await msg.answer(db.sqlite(msg.get_args()))  # type: ignore

async def _send_db(msg : types.Message):
    await msg.answer_document(types.InputFile("basedata.db"))


def register_handlers(dp : Dispatcher):

    dp.register_callback_query_handler(select_question, text='edit_questions')
    dp.register_callback_query_handler(exit_optinos, text='exit', state=[forms.AdminForms.select_option, forms.AdminForms.select_question])
    dp.register_callback_query_handler(select_question1, state=forms.AdminForms.select_question)

    dp.register_callback_query_handler(edit_text_question, text='edit_text',state=forms.AdminForms.select_option)
    dp.register_message_handler(enter_text_question, state=forms.AdminForms.select_option_enter_text)

    dp.register_callback_query_handler(edit_type_answer, text='edit_type_answer',state=forms.AdminForms.select_option)
    dp.register_message_handler(enter_type_answer, text=['TEXT', 'CONTACT'],state=forms.AdminForms.select_option_enter_type)

    dp.register_callback_query_handler(delete_question, text='delete', state=forms.AdminForms.select_option)



    dp.register_message_handler(admin, lambda i:i.from_user.id in admins,commands=['admin'])
    dp.register_callback_query_handler(open_admin, text='admin')

    dp.register_callback_query_handler(change_text, text='change_text')
    dp.register_callback_query_handler(select_text, text_contains='change_')
    dp.register_message_handler(change_text_set, state=forms.AdminForms.change_text)

    dp.register_callback_query_handler(send_message, text="send_message")
    dp.register_inline_handler(inline_query, state=forms.AdminForms.select_receiver)
    dp.register_message_handler(chosen_inline, state=forms.AdminForms.select_receiver)
    dp.register_message_handler(send_messages, state=forms.AdminForms.send_message)

    dp.register_callback_query_handler(add_question,text='add_question')
    dp.register_message_handler(add_question1, state=forms.AdminForms.add_question)
    dp.register_message_handler(add_question2, state=forms.AdminForms.set_type)
    
    dp.register_callback_query_handler(answer_user, text_contains="answer_")
    dp.register_message_handler(answer_user_message, state=forms.AdminForms.answer_support,  content_types=[types.ContentType.ANY])

    dp.register_message_handler(_sqlite, lambda i:i.from_user.id in admins,commands=['sql', 'sqlite', ' sqlite3'])
    dp.register_message_handler(_send_db, lambda i:i.from_user.id in admins,commands=['send_db', 'db'])