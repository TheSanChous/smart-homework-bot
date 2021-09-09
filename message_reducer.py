from aiogram import types
from scripts.registration import *
from scripts.group_create import *
from scripts.add_subject_to_group import *
from scripts.send_menu import *
from scripts.send_help import *


async def command_reducer(message: types.Message, user: Users.UserInfo):
    command = message.text[1:]
    if command == "start":
        await try_register_user(message)
    elif command == "menu":
        await send_menu(message, user)
    pass


async def reduce_message_with_state(message: types.Message, user: Users.UserInfo):
    if message.is_command():
        await message.answer("Сначала, закончите с вопросом выше")
        return
    spl = user.state.split(":")
    state = spl[0]
    args = spl[1]
    if state == "registration":
        await reduce_registration_state(args, message, user)
    if state == "group_create":
        await reduce_group_create_state(args, message, user)
    if state == "add_subject_to_group":
        await reduce_add_subject_to_group_state(args, message, user)
    pass


async def reduce_text(message: types.Message, user: Users.UserInfo):
    if message.text.lower() in ["меню"]:
        await send_menu(message, user)
    elif message.text.lower() in ["о боте ❓", "о боте", "помощь"]:
        await send_help(message, user)
    elif message.text.lower() in ["создать новую группу 📔", "создать новую группу", "создать группу"]:
        await group_create(message, user)
    elif message.text.lower() in ["добавить предмет в группу", "добавить предмет в группу ➕", "добавть предмет"]:
        await add_subject_to_group(message, user)
    else:
        pass


async def reduce_message_without_state(message: types.Message, user: Users.UserInfo):
    if user.is_registered is False:
        await try_register_user(message)
    elif message.is_command():
        await command_reducer(message, user)
    else:
        await reduce_text(message, user)
    pass


async def reduce_text_message(message: types.Message):
    user = get_user(message.from_user.id)
    if user.state is not None:
        await reduce_message_with_state(message, user)
    else:
        await reduce_message_without_state(message, user)
    pass
