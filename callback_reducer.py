from aiogram import types

from strings import strings
from users_repos import UserInfo, get_user
from callback_buttons import *


async def reduce_registration_callback(registration_state: str, call: types.CallbackQuery, user: UserInfo):
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
            await call.message.answer(strings["enter_group_code"])
            user.set_state("registration:enter_group_code")
        elif call.data == "create_group":
            await call.message.answer("2")


async def reduce_callback_with_state(call: types.CallbackQuery, user: UserInfo):
    spl = user.state.split(":")
    state = spl[0]
    args = spl[1]
    if state == "registration":
        await reduce_registration_callback(args, call, user)
    pass


async def reduce_callback_without_state(call: types.CallbackQuery, user: UserInfo):
    pass


async def reduce_callback(call: types.CallbackQuery):
    user = get_user(call.from_user.id)
    if user.state is not None:
        await reduce_callback_with_state(call, user)
