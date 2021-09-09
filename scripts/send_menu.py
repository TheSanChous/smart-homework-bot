from aiogram import types
from strings import strings
from db import *
from callback_buttons import get_menu_keyboard


async def send_menu(message: types.Message, user: Users.UserInfo):
    await message.answer(strings["menu"], reply_markup=get_menu_keyboard(user.type))
