from aiogram import Bot, types
from users_repos import UserInfo
import users_repos
from strings import strings
from callback_buttons import *
from scenarios import *


async def not_found_command(message: types.Message):
    await message.answer(strings["command_not_found"])


async def start_command(user: UserInfo, message: types.Message):
    if user is None:
        # user = users_repos.create_user(message.from_user.id)
        await message.answer(strings["welcome_new_user"])
    else:
        await message.answer(strings["welcome_user"])
    pass


async def menu_command(message: types.Message):
    await message.answer("menu")


async def command_reducer(user: UserInfo, command: str, message: types.Message):
    to_exec = command_list.get(command)
    if to_exec is None:
        await not_found_command(message)
    else:
        await to_exec(user, message)
    pass


command_list = {
    "/start": start_command,
    "/menu": menu_command,
}


async def reduce(user: UserInfo, message: types.Message):
    if user.state is not None:
        spl = user.state.split(" ")
        if len(spl) >= 1:
            if spl[0] == "registration":
                await register_user(message)
    elif message.is_command():
        await command_reducer(user, message.text, message)