from aiogram import Bot
from aiogram.types import *
from users_repos import *
import users_repos
from strings import strings
from callback_buttons import *


async def try_register_user(message: Message):
    user = get_user(message.from_user.id)
    if user.is_registered:
        await message.answer(strings["user_registered"])
    else:
        await message.answer("Здравствуйте! Прежде чем начать работу, ответьте пожалуйста на пару вопросов.")
        await message.answer("Введите ваше Имя:")
        user.set_state("registration:enter_first_name")


async def command_reducer(message: Message, user: UserInfo):
    command = message.text[1:]
    if command == "start":
        await try_register_user(message)
    pass


async def reduce_message_with_state(message: Message, user: UserInfo):
    if message.is_command():
        await message.answer("Сначала, закончите с вопросом выше")
        return
    spl = user.state.split(":")
    state = spl[0]
    args = spl[1:]
    if state == "registration":
        if args[0] == "enter_first_name":
            user.set_first_name(message.text)
            await message.answer(strings["enter_last_name"])
            user.set_state("registration:enter_last_name")
        if args[0] == "enter_last_name":
            user.set_last_name(message.text)
            await message.answer(strings["enter_user_type"], reply_markup=get_user_type_switch_keyboard())
            user.set_state("registration:user_type")
    pass


async def reduce_message_without_state(message: Message, user: UserInfo):
    if message.is_command():
        await command_reducer(message, user)
    pass


async def reduce_text_message(message: Message):
    user = get_user(message.from_user.id)
    if user.state is not None:
        await reduce_message_with_state(message, user)
    else:
        await reduce_message_without_state(message, user)
    pass
