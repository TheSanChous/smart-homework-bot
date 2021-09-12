from .message_reducer import *
from .callback_reducer import *
from aiogram import types
from callback_buttons import get_user_groups_keyboard
from db.Users import UserInfo


async def add_homework(message: types.Message, user: UserInfo):
    if len(user.groups) == 0:
        await message.answer("У вас нет групп, для которых можно было бы добавить предмет. Сначала создайте группу.")
        return
    await message.answer("Выберите группу, которой нужно добавить задание", reply_markup=get_user_groups_keyboard(user))
    user.set_state("add_homework:select_group")