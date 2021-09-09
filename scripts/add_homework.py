from aiogram import types
from strings import strings
from callback_buttons import get_user_groups_keyboard, get_group_subjects_switch_keyboard
from db import *


async def add_homework(message: types.Message, user: Users.UserInfo):
    if len(user.groups) == 0:
        await message.answer("У вас нет групп, для которых можно было бы добавить предмет. Сначала создайте группу.")
        return
    await message.answer("Выберите группу, которой нужно добавить задание", reply_markup=get_user_groups_keyboard(user))
    user.set_state("add_homework:select_group")


async def reduce_add_homework_state(state: str, message: types.Message, user: Users.UserInfo):
    pass


async def reduce_add_homework_state_callback(state: str, call: types.CallbackQuery, user: Users.UserInfo):
    if state == "select_group":
        group = get_group(int(call.data))
        if group is None:
            await call.answer(strings["unknown_error"])
            user.set_state(None)
            return
        if len(group.subjects) == 0:
            await call.answer("У вас нет предметов, для которых вы бы могли добавить домашнее задание..")
            user.set_state(None)
            return
        user.set_selected_group(group)
        await call.message.answer("Выберите предмет, для которого вы хотите добавить домашнее задание",
                                  reply_markup=get_group_subjects_switch_keyboard(group))
        user.set_state("add_homework:select_subject")
        return
    elif state == "select_subject":
        await call.message.edit_reply_markup(get_group_subjects_switch_keyboard(user.selected_group, int(call.data)))
        subject = get_subject(int(call.data))
        ...
