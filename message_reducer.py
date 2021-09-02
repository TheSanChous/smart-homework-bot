from aiogram import Bot, types
import users_repos
from strings import *


async def not_found_command(message: types.Message):
    await message.answer(command_not_found)


async def start_command(message: types.Message):
    user = users_repos.get_user(message.from_user.id)
    if user is None:
        users_repos.create_user(message.from_user.id)
        await message.answer(welcome_new_user)
    else:
        await message.answer(welcome_user)
    pass


async def menu_command(message: types.Message):
    await message.answer("menu")


command_list = {
    "/start": start_command,
    "/menu": menu_command,
}


async def reduce(message: types.Message):
    if message.is_command():
        await command_reducer(message.text, message)


async def command_reducer(command: str, message: types.Message):
    to_exec = command_list.get(command)
    if to_exec is None:
        await not_found_command(message)
    else:
        await to_exec(message)
    pass

