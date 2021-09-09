from aiogram import types
from strings import strings
from db import *
from callback_buttons import get_user_type_switch_keyboard, get_join_or_create_group_keyboard, \
    get_enter_subject_description_cancel_keyboard, get_user_groups_keyboard
from scripts.group_create import group_create
from scripts.join_group import join_group


async def reduce_group_create_callback(group_create_state: str, call: types.CallbackQuery, user: Users):
    pass


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


async def reduce_add_subject_to_group_state(args: str, call: types.CallbackQuery, user: Users.UserInfo):
    if args == "group_switch":
        group = get_group(call.data)
        if group is None:
            await call.message.answer("Ошибка, группа не найдена.")
            return
        await call.message.edit_reply_markup(get_user_groups_keyboard(user, selected=call.data))
        await call.message.answer(strings["enter_subject_name"])
        user.set_selected_group(group)
        user.set_state("add_subject_to_group:enter_subject_name")
    if args == "enter_subject_description":
        if call.data == "cancel_enter_subject_description":
            await call.message.edit_reply_markup(get_enter_subject_description_cancel_keyboard(True))
            await call.message.answer(strings["subject_added_successful"])
            user.set_state(None)


async def reduce_callback_with_state(call: types.CallbackQuery, user: Users.UserInfo):
    spl = user.state.split(":")
    state = spl[0]
    args = spl[1]
    if state == "registration":
        await reduce_registration_callback(args, call, user)
    if state == "add_subject_to_group":
        await reduce_add_subject_to_group_state(args, call, user)
    pass


async def reduce_callback_without_state(call: types.CallbackQuery, user: Users.UserInfo):
    pass


async def reduce_callback(call: types.CallbackQuery):
    user = get_user(call.from_user.id)
    if user.state is not None:
        await reduce_callback_with_state(call, user)
