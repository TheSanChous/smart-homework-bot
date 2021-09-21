from aiogram import types, Bot
from resources.strings import strings
from resources.keyboards import get_user_groups_keyboard, get_group_subjects_switch_keyboard, \
    get_add_homework_types_keyboard
from resources.keyboards.calendar import create_calendar, process_calendar_selection
from db import *


async def send_homework(bot: Bot, user: Users.UserInfo):
    users = get_group_students_id(user.selected_group)
    for to_user in users:
        await bot.send_message(to_user.user_id, f"Домашнее задание по предммету {user.selected_subject.name}:\n{user.selected_homework.description}")


async def reduce_add_homework_select_group_state_callback(call: types.CallbackQuery, user: Users.UserInfo):
    await call.message.edit_reply_markup(get_user_groups_keyboard(user, selected=call.data))
    if call.data == "cancel":
        await call.message.answer("Добавление задания отменено.")
        user.clear_selected()
        return
    group = get_group(int(call.data))
    if group is None:
        await call.answer(strings["unknown_error"])
        user.set_state(None)
        return
    if len(group.subjects) == 0:
        await call.message.answer(
            "В этой группе нет предметов, чтобы можно было добавить домашнее задание..\nДобавить предмет - /add_subject")
        user.set_state(None)
        return
    user.set_selected_group(group)
    await call.message.answer("Выберите предмет, для которого вы хотите добавить домашнее задание",
                              reply_markup=get_group_subjects_switch_keyboard(group))
    user.set_state("add_homework:select_subject")
    return


async def reduce_add_homework_select_subject_state_callback(call: types.CallbackQuery, user: Users.UserInfo):
    if call.data == "cancel":
        await call.message.edit_reply_markup(get_group_subjects_switch_keyboard(user.selected_group, -1))
        await call.message.answer("Добавление задания отменено.")
        user.clear_selected()
        return
    subject = get_subject(int(call.data))
    await call.message.edit_reply_markup(
        get_group_subjects_switch_keyboard(user.selected_group, selected_id=subject.subject_id))
    user.set_selected_subject(subject)
    await call.message.answer("Выберите дату домашнего задания:",
                              reply_markup=create_calendar("add_homework:select_date"))
    user.set_state("add_homework:select_date")


async def reduce_add_homework_select_date_state_callback(state: str, call: types.CallbackQuery, user: Users.UserInfo):
    is_day, date = await process_calendar_selection("add_homework:select_date", call)
    if is_day:
        if user.selected_homework is None:
            user.set_selected_homework(create_homework(user.selected_subject, "", date))
        else:
            user.selected_homework.set_date(date)
        await call.message.edit_text(f"Выберите дату домашнего задания:\n<b>{date.day} - {date.month} - {date.year}</b>")
        user.set_state("add_homework:add")
        await call.message.answer("Выберите один из вариантов ниже",
                                  reply_markup=get_add_homework_types_keyboard(selected=[]))
    pass


async def reduce_add_homework_add_state_callback(call: types.CallbackQuery, user: Users.UserInfo):
    selected = call.data
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
        await send_homework(call.bot, user)
        user.clear_selected()
        return
    selected_type = call.data
    selected.append(selected_type)
    if selected_type == "text":
        await call.message.answer("Напишите ваше сообщение:")
        user.set_state("add_homework:add:text")


async def reduce_add_homework_state_callback(state: str, call: types.CallbackQuery, user: Users.UserInfo):
    if state == "select_group":
        await reduce_add_homework_select_group_state_callback(call, user)
    elif state == "select_subject":
        await reduce_add_homework_select_subject_state_callback(call, user)
    elif state == "select_date":
        await reduce_add_homework_select_date_state_callback(state, call, user)
    elif state == "add":
        await reduce_add_homework_add_state_callback(call, user)
    pass
