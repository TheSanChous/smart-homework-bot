from aiogram import types
from resources.strings import strings
from db import *
from resources.keyboards import get_enter_subject_description_cancel_keyboard, get_user_groups_keyboard


async def reduce_add_subject_to_group_cancel_state_callback(call: types.CallbackQuery, user: Users.UserInfo):
    await call.message.edit_reply_markup(get_user_groups_keyboard(user, selected=call.data))
    await call.message.answer("Добавление предмета отменено.")
    user.set_state(None)
    pass


async def reduce_add_subject_to_group_group_switch_state_callback(call: types.CallbackQuery, user: Users.UserInfo):
    group = get_group(call.data)
    if group is None:
        await call.message.answer("Ошибка, группа не найдена.")
        return
    await call.message.edit_reply_markup(get_user_groups_keyboard(user, selected=call.data))
    await call.message.answer(strings["enter_subject_name"])
    user.set_selected_group(group)
    user.set_state("add_subject_to_group:enter_subject_name")
    pass


async def reduce_add_subject_to_group_enter_subject_description_state_callback(call: types.CallbackQuery, user: Users.UserInfo):
    if call.data == "cancel_enter_subject_description":
        await call.message.edit_reply_markup(get_enter_subject_description_cancel_keyboard(True))
        await call.message.answer(strings["subject_added_successful"])
        user.set_state(None)
    pass


async def reduce_add_subject_to_group_state_callback(args: str, call: types.CallbackQuery, user: Users.UserInfo):
    if call.data == "cancel":
        await reduce_add_subject_to_group_cancel_state_callback(call, user)
        return
    elif args == "group_switch":
        await  reduce_add_subject_to_group_group_switch_state_callback(call, user)
    elif args == "enter_subject_description":
        await reduce_add_subject_to_group_enter_subject_description_state_callback(call, user)
    pass
