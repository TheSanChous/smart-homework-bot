from aiogram.types import *
from resources.keyboards import get_menu_keyboard
from db import get_group
from db.Users import UserInfo
from resources.strings import strings


async def reduce_join_group_enter_group_code_state(state: str, message: Message, user: UserInfo):
    group = get_group(message.text)
    if group is None:
        await message.answer(strings["incorrect_group_id"])
        return
    user.add_group(group)
    await message.answer(strings["successful_join_to_group"].format(group_name=group.name),
                         reply_markup=get_menu_keyboard(user.type))
    user.set_state(None)


async def reduce_join_group_state(state: str, message: Message, user: UserInfo):
    if state == "enter_group_code":
        await reduce_join_group_enter_group_code_state(state, message, user)
    pass
