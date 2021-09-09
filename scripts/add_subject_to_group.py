from aiogram import types
from strings import strings
from db import *
from callback_buttons import get_enter_subject_description_cancel_keyboard, get_user_groups_keyboard


async def add_subject_to_group(message: types.Message, user: Users.UserInfo):
    if len(user.groups) == 0:
        await message.answer("У вас нет групп, для которых можно было бы добавить предмет. Сначала создайте группу.")
        return
    else:
        await message.answer(strings["chose_group_for_add_subject"], reply_markup=get_user_groups_keyboard(user))
        user.set_state("add_subject_to_group:group_switch")


async def reduce_add_subject_to_group_state(add_subject_to_group_state: str, message: types.Message, user: Users.UserInfo):
    if add_subject_to_group_state == "enter_subject_name":
        subject = create_subject(message.text, user.selected_group)
        await message.answer(strings["enter_subject_description"],
                             reply_markup=get_enter_subject_description_cancel_keyboard())
        user.set_state("add_subject_to_group:enter_subject_description")
        user.set_selected_subject(subject)
    elif add_subject_to_group_state == "enter_subject_description":
        await message.answer(strings["subject_description_added"])
        await message.answer(strings["subject_added_successful"])
        user.selected_subject.set_description(message.text)
        user.set_selected_subject(None)
        user.set_state(None)
    pass