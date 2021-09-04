from aiogram.types import *
from users_repos import *
from callback_buttons import *
from users_repos import UserInfo
from strings import strings


async def check_register_user(message: Message) -> UserInfo:
    user = get_user(message.chat.id)
    if user is None:
        await message.answer(strings["user_not_registered"], reply_markup=get_register_keyboard())
        return None
    else:
        return user


async def register_user(message: Message):
    user = get_user(message.chat.id)
    if user is None:
        user = create_user(message.chat.id)

    if user.state is None or user.state == "":
        await message.answer(strings["enter_first_name"])
        user.set_state(f"registration enter_first_name")
    elif user.state == "registration enter_first_name":
        user.set_first_name(message.text)
        await message.answer(strings["enter_last_name"])
        user.set_state(f"registration enter_last_name")
    elif user.state == "registration enter_last_name":
        user.set_last_name(message.text)
        await message.answer(strings["register_successful"])
        user.set_state(None)
        user.set_registered(True)
    pass
