from aiogram import types
from strings import strings
from db import *


async def send_help(message: types.Message, user: Users.UserInfo):
    await message.answer(strings["help"])
