from .message_reducer import *
from aiogram import types
from resources.strings import strings
from db import *


async def registration_join_group(message: types.Message, user: Users.UserInfo):
    await message.answer(strings["enter_group_code"])
    user.set_state("registration:enter_group_code")


async def join_group(message: types.Message, user: Users.UserInfo):
    await message.answer(strings["enter_group_code"])
    user.set_state("join_group:enter_group_code")
    pass
