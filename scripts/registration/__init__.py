from .message_reducer import *
from .callback_reducer import *
from aiogram import types
from resources.strings import strings
from db import *


async def try_register_user(message: types.Message):
    user = get_user(message.from_user.id)
    if user.is_registered:
        await message.answer(strings["user_registered"])
    else:
        await message.answer("Здравствуйте! Прежде чем начать работу, ответьте пожалуйста на пару вопросов.")
        await message.answer("Введите ваше Имя:")
        user.set_state("registration:enter_first_name")
