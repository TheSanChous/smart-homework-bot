from aiogram import types
from scenarios import *
from users_repos import *
from callback_buttons import *


async def reduce_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "start_register":
        await register_user(callback_query.message)
        await callback_query.message.edit_reply_markup(get_register_keyboard(enable=False))
    elif callback_query.data == "retry_register":
        await callback_query.answer(text=strings["user_registered"], show_alert=True)
