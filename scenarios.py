from aiogram.types import *
from users_repos import UserInfo
from strings import strings


async def register_user(user: UserInfo, message: Message):
    print(user.state)
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
