from create_bot import db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

menu_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Я подтверждаю ▶️", callback_data='i_approve')]
    ]
)

form_conditional = ReplyKeyboardMarkup(
    [
        ["online", "offline"]
    ], resize_keyboard=True
)

contact = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("Номер телефона",request_contact=True)]
    ]
)

admin_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("ОТПРАВИТЬ СООБЩЕНИЕ", callback_data='send_message')],
        [InlineKeyboardButton("ИЗМЕНИТЬ ТЕКСТ", callback_data="change_text")],
        [InlineKeyboardButton("ДОБАВИТЬ ВОПРОС", callback_data='add_question')]
    ]
)

def list_texts ():
    markup = InlineKeyboardMarkup()
    for key, in db.sqlite('SELECT key FROM Texts'):
        markup.add(InlineKeyboardButton(key, callback_data=f'change_{key}'))
    markup.add(InlineKeyboardButton("НАЗАД", callback_data='admin'))
    return markup