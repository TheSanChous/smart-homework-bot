from aiogram import types
from users_repos import user_types
from strings import strings


def get_user_type_switch_keyboard():
    keyboard = types.InlineKeyboardMarkup(2)
    for user_type in user_types:
        button = types.InlineKeyboardButton(text=strings[user_type], callback_data=user_type)
        keyboard.add(button)
    return keyboard


def get_join_or_create_group_keyboard():
    keyboard = types.InlineKeyboardMarkup(2)
    create_button = types.InlineKeyboardButton(text=strings["create_group"], callback_data="create_group")
    join_button = types.InlineKeyboardButton(text=strings["join_group"], callback_data="join_group")
    keyboard.add(create_button, join_button)
    return keyboard
