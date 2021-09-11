from aiogram import types
from strings import strings
from callback_buttons import get_user_groups_keyboard, get_group_subjects_switch_keyboard, \
    get_add_homework_types_keyboard
from db import *


async def add_homework(message: types.Message, user: Users.UserInfo):
    if len(user.groups) == 0:
        await message.answer("У вас нет групп, для которых можно было бы добавить предмет. Сначала создайте группу.")
        return
    await message.answer("Выберите группу, которой нужно добавить задание", reply_markup=get_user_groups_keyboard(user))
    user.set_state("add_homework:select_group")


async def reduce_add_homework_state(state: str, message: types.Message, user: Users.UserInfo):
    if state == "add:text":
        if user.selected_homework is None:
            user.set_selected_homework(create_homework(user.selected_subject, message.text))
        else:
            user.selected_homework.set_description(message.text)
        selected = list()
        if user.selected_homework.description is not None:
            selected.append("text")
        user.set_state("add_homework:add")
        await message.answer("Текстовое описание добавлено! Выберите один из вариантов ниже, чтобы добавить больше:",
                             reply_markup=get_add_homework_types_keyboard(selected=selected, complete=True))
    pass


async def reduce_add_homework_state_callback(state: str, call: types.CallbackQuery, user: Users.UserInfo):
    if state == "select_group":
        await call.message.edit_reply_markup(get_user_groups_keyboard(user, selected=call.data))
        if call.data == "cancel":
            user.clear_selected()
            await call.message.answer("Добавление задания отменено.")
            return
        group = get_group(int(call.data))
        if group is None:
            await call.answer(strings["unknown_error"])
            user.set_state(None)
            return
        if len(group.subjects) == 0:
            await call.message.answer("В этой группе нет предметов, чтобы можно было добавить домашнее задание..\nДобавить предмет - /add_subject")
            user.set_state(None)
            return
        user.set_selected_group(group)
        await call.message.answer("Выберите предмет, для которого вы хотите добавить домашнее задание",
                                  reply_markup=get_group_subjects_switch_keyboard(group))
        user.set_state("add_homework:select_subject")
        return
    elif state == "select_subject":
        if call.data == "cancel":
            await call.message.edit_reply_markup(get_group_subjects_switch_keyboard(user.selected_group, -1))
            await call.message.answer("Добавление задания отменено.")
            user.clear_selected()
            return
        subject = get_subject(int(call.data))
        await call.message.edit_reply_markup(get_group_subjects_switch_keyboard(user.selected_group, selected_id=subject.subject_id))
        user.set_selected_subject(subject)
        await call.message.answer("Выберите один из вариантов ниже", reply_markup=get_add_homework_types_keyboard(selected=[]))
        user.set_state("add_homework:add")
    elif state == "add":
        selected = list()
        if user.selected_homework is not None:
            if user.selected_homework.description is not None:
                selected.append("text")
        if call.data == "cancel":
            selected.append("cancel")
            await call.message.edit_reply_markup(get_add_homework_types_keyboard(selected=selected))
            await call.message.answer("Добавление задания отменено.")
            if user.selected_homework is not None:
                user.selected_homework.delete()
            user.clear_selected()
            return
        elif call.data == "submit":
            selected.append("submit")
            await call.message.edit_reply_markup(get_add_homework_types_keyboard(selected=selected, complete=True))
            await call.message.answer("Задание добавлено!")
            user.clear_selected()
            return
        selected_type = call.data
        selected.append(selected_type)
        if selected_type == "text":
            await call.message.answer("Напишите ваше сообщение:")
            user.set_state("add_homework:add:text")
