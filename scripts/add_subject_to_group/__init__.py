from .message_reducer import *
from .callback_reducer import *
from aiogram import types
from resources.strings import strings
from db import *
from resources.keyboards import get_user_groups_keyboard


async def add_subject_to_group(message: types.Message, user: Users.UserInfo):
    if len(user.groups) == 0:
        await message.answer("У вас нет групп, для которых можно было бы добавить предмет. Сначала создайте группу.")
        return
    else:
        await message.answer(strings["chose_group_for_add_subject"], reply_markup=get_user_groups_keyboard(user))
        user.set_state("add_subject_to_group:group_switch")
    pass
