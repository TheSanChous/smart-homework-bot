from aiogram import types
from scenarios import *
from users_repos import *


async def reduce_callback(callback_query: types.CallbackQuery):
    user = get_user(callback_query.from_user.id)
    if callback_query.data == "start_register":
        await register_user(user, callback_query.message)
        await callback_query.message.edit_reply_markup(None)
