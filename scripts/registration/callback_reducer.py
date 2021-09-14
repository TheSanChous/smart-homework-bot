from aiogram.types import *
from db import Users
from resources.keyboards import get_user_type_switch_keyboard, get_join_or_create_group_keyboard
from scripts.group_create import group_create
from scripts.join_group import registration_join_group
from resources.strings import strings


async def reduce_registration_user_type_callback(call: CallbackQuery, user: Users.UserInfo):
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
    pass


async def reduce_registration_join_or_create_group_callback(call: CallbackQuery, user: Users.UserInfo):
    if call.data == "join_group":
        await call.message.edit_reply_markup(get_join_or_create_group_keyboard("join"))
        await registration_join_group(call.message, user)
    elif call.data == "create_group":
        await call.message.edit_reply_markup(get_join_or_create_group_keyboard("create"))
        await group_create(call.message, user)
    pass


async def reduce_registration_callback(registration_state: str, call: CallbackQuery, user: Users.UserInfo):
    if registration_state == "user_type":
        await reduce_registration_user_type_callback(call, user)
    elif registration_state == "join_or_create_group":
        await reduce_registration_join_or_create_group_callback(call, user)
    pass

