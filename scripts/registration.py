from aiogram import types

from scripts.group_create import group_create
from scripts.join_group import join_group
from strings import strings

from db import *

from callback_buttons import get_menu_keyboard, get_user_type_switch_keyboard, get_join_or_create_group_keyboard


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


async def reduce_registration_callback(registration_state: str, call: types.CallbackQuery, user: Users.UserInfo):
    if registration_state == "user_type":
        user.set_type(call.data)
        if user.type == "student":
            await call.message.edit_reply_markup(get_user_type_switch_keyboard("student"))
            await call.message.answer(strings["enter_group_code"])
            user.set_state("registration:enter_group_code")
        elif user.type == "teacher":
            await call.message.edit_reply_markup(get_user_type_switch_keyboard("teacher"))
            await call.message.answer(strings["join_or_create_group"],
                                      reply_markup=get_join_or_create_group_keyboard())
            user.set_state("registration:join_or_create_group")
    if registration_state == "join_or_create_group":
        if call.data == "join_group":
            await call.message.edit_reply_markup(get_join_or_create_group_keyboard("join"))
            await join_group(call.message, user)
        elif call.data == "create_group":
            await call.message.edit_reply_markup(get_join_or_create_group_keyboard("create"))
            await group_create(call.message, user)

