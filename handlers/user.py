import markups, forms, create_bot
from create_bot import bot, db
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from datetime import datetime

admins = (367961212,1835953916)

async def start(message : types.Message):
    await message.answer(
        """Вы регистрируетесь на курс ученичества IPSI, который проходит в формате online (3 месяца 3 дня в неделю) и offline (5 месяцев стационарного обучения на базах служениях). 

Дата старта курса - 3 Апреля 2022 года.

Подробнее об онлайн курсе можно узнать тут:
https://ipsischool.com/

Для начала, подтвердите свое согласие на сбор и обработку своих персональных данных, нажав внизу кнопку ""Я подтверждаю"" 👇""",
        reply_markup=markups.menu_markup
    )
    print('/start', message.from_user.id)

async def on_message(message : types.Message):
    await bot.send_message(
        367961212,
        f""" <b>User</b> : <b>{message.from_user.username}</b>
<b>User ID</b> : <i>{message.from_user.id}</i>
Message :
{message.text}
""", parse_mode='HTML', reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton('ОТВЕТИТЬ', callback_data=f'answer_{message.from_user.id}_{message.message_id}')]])
    )

# ===================== REGISTER ===================== #

async def i_approve(callback : types.CallbackQuery, state : FSMContext):
    
    try: await callback.answer()
    except Exception: pass
    
    if db.get_user_info(callback.from_user.id):
        return

    await forms.RegisterForms.registrate.set()
    questions = db.get_questions()
    await callback.message.answer(questions[0][0])
    await state.update_data(
        questions=questions,
        answers=[],
        step=0,
        content_type=questions[0][2]
    )

async def register(message : types.Message, state : FSMContext):
    data = await state.get_data()
    try:
        step = data.get('step',0)
        if message.content_type == data.get('content_type', 'TEXT').lower():
            data.get('answers', []).append(message.text if data.get('content_type') == 'TEXT' else message.contact.phone_number)
            await message.answer(
                data.get('questions')[step+1][0],
                reply_markup=markups.contact if data.get('questions')[step+1][2] == 'CONTACT' else None
            )
            
            await state.update_data(
                {
                    'step'            : step + 1,
                    'answers'         : data.get('answers', []),
                    'content_type'    : data.get('questions')[step+1][2],
                }
            )
        else:
            await message.answer(
                data.get('questions')[step][0],
                reply_markup=markups.contact if data.get('questions')[step][2] == 'CONTACT' else None
            )
    except IndexError:
        await state.finish()
        await message.answer("""Ваша анкета принята 🙌

*ONLINE курс* начнется 3 Апреля 2022 года, детали будут опубликованы немного позже в телеграм канале.

Вступайте в него по следующей ссылке:
(ссылка пока что недоступна)

*OFFLINE курс* 
После регистрации с вами свяжется куратор и сообщит детали.

👉 При возникновении вопросов обращайтесь в телеграм аккаунт @ipsischool.

До встречи на ИПСИ 👋""", reply_markup=types.ReplyKeyboardRemove())
        
        db.insert_user_data(message.from_user.full_name, message.from_user.username, ', '.join(data.get('answers', [])), message.from_user.id)
        await create_bot.user_workspace.append_row([
            db.get_num,
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.full_name,
            datetime.now().strftime('%d.%m.%Y - %H:%M'),
            *data.get('answers')
        ])

# ===================== REGISTER HANDLERS ===================== #

def register_handlers(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])

    dp.register_message_handler(on_message, lambda i: db.get_user_info(i.from_user.id) and i.from_user.id not in admins)

    dp.register_callback_query_handler(i_approve, text='i_approve')
    dp.register_message_handler(register,content_types=[types.ContentType.TEXT,types.ContentType.CONTACT],state=forms.RegisterForms.registrate)