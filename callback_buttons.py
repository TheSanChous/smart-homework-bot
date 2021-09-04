from aiogram import types
from strings import buttons


def get_register_keyboard(enable: bool = True):
    keyboard = types.InlineKeyboardMarkup(1)
    button = buttons["register"]
    register_button = types.InlineKeyboardButton(text=button["text"], callback_data=button["data"])
    if not enable:
        register_button.callback_data = button["disable"]
    keyboard.add(register_button)
    return keyboard
