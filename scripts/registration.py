from aiogram import types
from strings import strings
from db import *
from callback_buttons import get_menu_keyboard, get_user_type_switch_keyboard


async def try_register_user(message: types.Message):
    user = get_user(message.from_user.id)
    if user.is_registered:
        await message.answer(strings["user_registered"])
    else:
        await message.answer("Здравствуйте! Прежде чем начать работу, ответьте пожалуйста на пару вопросов.")
        await message.answer("Введите ваше Имя:")
        user.set_state("registration:enter_first_name")


async def reduce_registration_state(registration_state: str, message: types.Message, user: Users.UserInfo):
    if registration_state == "enter_first_name":
        user.set_first_name(message.text)
        await message.answer(strings["enter_last_name"])
        user.set_state("registration:enter_last_name")
    elif registration_state == "enter_last_name":
        user.set_last_name(message.text)
        await message.answer(strings["enter_user_type"], reply_markup=get_user_type_switch_keyboard())
        user.set_state("registration:user_type")
    elif registration_state == "enter_group_code":
        group = get_group(message.text)
        if group is None:
            await message.answer(strings["incorrect_group_id"])
            return
        user.add_group(group)
        await message.answer(strings["successful_join_to_group"].format(group_name=group.name),
                             reply_markup=get_menu_keyboard(user.type))
        user.set_state(None)
        user.set_registered(True)