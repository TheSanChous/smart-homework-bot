from aiogram import types
from strings import buttons


def get_register_keyboard():
    keyboard = types.InlineKeyboardMarkup(1)
    button = buttons["register"]
    register_button = types.InlineKeyboardButton(button["text"], callback_data=button["data"])
    keyboard.add(register_button)
    return keyboard
