from aiogram import types
from callback_buttons import get_add_homework_types_keyboard
from db import Users, create_homework
from .callback_reducer import get_user_selected_add_types


async def reduce_add_homework_text_state(message: types.Message, user: Users.UserInfo):
    if user.selected_homework is None:
        user.set_selected_homework(create_homework(user.selected_subject, message.text))
    else:
        user.selected_homework.set_description(message.text)
    selected = get_user_selected_add_types(user)
    await message.answer("Текстовое описание добавлено! Выберите один из вариантов ниже, чтобы добавить больше:",
                         reply_markup=get_add_homework_types_keyboard(selected=selected, complete=True))
    user.set_state("add_homework:add")


async def reduce_add_homework_state(state: str, message: types.Message, user: Users.UserInfo):
    if state == "add:text":
        await reduce_add_homework_text_state(message, user)
    pass
