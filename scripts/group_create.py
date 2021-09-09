from aiogram import types
from strings import strings
from db import *
from callback_buttons import get_menu_keyboard


async def group_create(message: types.Message, user: Users.UserInfo):
    await message.answer(strings["enter_group_name"])
    user.set_state("group_create:enter_group_name")


async def reduce_group_create_state(group_create_state: str, message: types.Message, user: Users.UserInfo):
    if group_create_state == "enter_group_name":
        group = create_group(message.text)
        user.add_group(group)
        await message.answer(strings["group_created_successful"].format(group_name=group.name,
                                                                        group_code=group.group_id),
                             reply_markup=get_menu_keyboard(user.type))
        user.set_state(None)
        if user.is_registered is False:
            user.set_registered(True)
        user.set_state(None)
    pass
