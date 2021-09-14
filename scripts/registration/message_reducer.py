from aiogram.types import *
from db import Users, get_group
from resources.keyboards import get_menu_keyboard, get_user_type_switch_keyboard
from resources.strings import strings


async def reduce_registration_enter_first_name_state(message: Message, user: Users.UserInfo):
    user.set_first_name(message.text)
    await message.answer(strings["enter_last_name"])
    user.set_state("registration:enter_last_name")
    pass


async def reduce_registration_enter_last_name_state(message: Message, user: Users.UserInfo):
    user.set_last_name(message.text)
    await message.answer(strings["enter_user_type"], reply_markup=get_user_type_switch_keyboard())
    user.set_state("registration:user_type")
    pass


async def reduce_registration_enter_group_code_state(message: Message, user: Users.UserInfo):
    group = get_group(message.text)
    if group is None:
        await message.answer(strings["incorrect_group_id"])
        return
    user.add_group(group)
    await message.answer(strings["successful_join_to_group"].format(group_name=group.name),
                         reply_markup=get_menu_keyboard(user.type))
    user.set_state(None)
    user.set_registered(True)
    pass


async def reduce_registration_state(registration_state: str, message: Message, user: Users.UserInfo):
    if registration_state == "enter_first_name":
        await reduce_registration_enter_first_name_state(message, user)
    elif registration_state == "enter_last_name":
        await reduce_registration_enter_last_name_state(message, user)
    elif registration_state == "enter_group_code":
        await reduce_registration_enter_group_code_state(message, user)
    pass
