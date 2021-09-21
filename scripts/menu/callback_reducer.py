from aiogram import types
from db import Users
from scripts import add_homework, add_subject_to_group


async def reduce_menu_callback(call: types.CallbackQuery, user: Users.UserInfo):
    data = call.data
    if data == "add_homework":
        await add_homework(call.message, user)
    elif data == "add_subject":
        await add_subject_to_group(call.message, user)
    pass
