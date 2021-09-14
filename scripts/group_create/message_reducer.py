from aiogram.types import *
from db import Users, create_group
from resources.strings import strings
from resources.keyboards import get_menu_keyboard


async def reduce_enter_group_name_state(state: str, message: Message, user: Users.UserInfo):
    group = create_group(message.text)
    user.add_group(group)
    await message.answer(strings["group_created_successful"].format(group_name=group.name, group_code=group.group_id),
                         reply_markup=get_menu_keyboard(user.type))
    user.set_state(None)
    if user.is_registered is False:
        user.set_registered(True)
    user.set_state(None)


async def reduce_group_create_state(group_create_state: str, message: Message, user: Users.UserInfo):
    if group_create_state == "enter_group_name":
        await reduce_enter_group_name_state(group_create_state, message, user)
    pass
