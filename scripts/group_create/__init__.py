from .message_reducer import *
from aiogram import types
from resources.strings import strings
from db import *


async def group_create(message: types.Message, user: Users.UserInfo):
    await message.answer(strings["enter_group_name"])
    user.set_state("group_create:enter_group_name")
