from aiogram import types

from strings import strings
from users_repos import UserInfo, get_user
from callback_buttons import *


async def reduce_callback_with_state(call: types.CallbackQuery, user: UserInfo):
    spl = user.state.split(":")
    state = spl[0]
    args = spl[1:]
    if state == "registration":
        if args[0] == "user_type":
            user.set_type(call.data)
            if user.type == "student":
                await call.message.answer(strings["enter_group_code"])
                user.set_state("registration:enter_group_code")
            elif user.type == "teacher":
                await call.message.answer(strings["join_or_create_group"],
                                          reply_markup=get_join_or_create_group_keyboard())
                user.set_state("registration:join_or_create_group")
        if args[0] == "join_or_create_group":
            if call.data == "join_group":
                await call.message.answer("1")
            elif call.data == "create_group":
                await call.message.answer("2")

    pass


async def reduce_callback_without_state(call: types.CallbackQuery, user: UserInfo):
    pass


async def reduce_callback(call: types.CallbackQuery):
    user = get_user(call.from_user.id)
    if user.state is not None:
        await reduce_callback_with_state(call, user)
