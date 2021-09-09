from aiogram import types
from strings import strings
from db import *
from callback_buttons import get_menu_keyboard, get_enter_subject_description_cancel_keyboard, get_user_groups_keyboard, \
    get_user_type_switch_keyboard


async def send_help(message: types.Message, user: Users.UserInfo):
    await message.answer(strings["help"])
