from aiogram import types
from resources.strings import strings
from db import *
from resources.keyboards import get_enter_subject_description_cancel_keyboard


async def reduce_add_subject_to_group_enter_subject_name_state(message: types.Message, user: Users.UserInfo):
    subject = create_subject(message.text, user.selected_group)
    await message.answer(strings["enter_subject_description"],
                         reply_markup=get_enter_subject_description_cancel_keyboard())
    user.set_state("add_subject_to_group:enter_subject_description")
    user.set_selected_subject(subject)
    pass


async def reduce_add_subject_to_group_enter_subject_description_state(message: types.Message, user: Users.UserInfo):
    await message.answer(strings["subject_description_added"])
    await message.answer(strings["subject_added_successful"])
    user.selected_subject.set_description(message.text)
    user.set_selected_subject(None)
    user.set_state(None)
    pass


async def reduce_add_subject_to_group_state(add_subject_to_group_state: str, message: types.Message, user: Users.UserInfo):
    if add_subject_to_group_state == "enter_subject_name":
        await reduce_add_subject_to_group_enter_subject_name_state(message, user)
    elif add_subject_to_group_state == "enter_subject_description":
        await reduce_add_subject_to_group_enter_subject_description_state(message, user)
    pass
