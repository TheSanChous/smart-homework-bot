from aiogram import types
from resources.strings import strings
from db import *
from resources.keyboards import get_menu_keyboard
from resources.keyboards.menu_inline_keyboard import get_menu_inline_keyboard


async def send_menu(message: types.Message, user: Users.UserInfo):
    user.set_state("menu")
    await message.answer(text=strings["menu"], reply_markup=get_menu_inline_keyboard())
    pass
