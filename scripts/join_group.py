from aiogram import types
from strings import strings
from db import *


async def join_group(message: types.Message, user: Users.UserInfo):
    await message.answer(strings["enter_group_code"])
    user.set_state("registration:enter_group_code")
