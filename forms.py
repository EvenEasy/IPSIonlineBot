from aiogram.dispatcher.filters.state import State, StatesGroup

class RegisterForms(StatesGroup):
    registrate = State()
    registrate_contact = State()

class AdminForms(StatesGroup):
    change_text = State()

    select_receiver = State()
    send_message = State()

    add_question = State()
    set_type = State()

    answer_support = State()
