from aiogram.types import *
from ..strings import strings
from . import KEYBOARD_OFF


def get_menu_inline_keyboard(selected: str = None):
    add_homework_button = InlineKeyboardButton(text=strings["add_homework"] + (" ✅" if selected == "add_homework" else ""),
                                               callback_data=KEYBOARD_OFF if selected else "add_homework")
    add_subject_to_group_button = InlineKeyboardButton(text=strings["add_subject"],
                                                       callback_data=KEYBOARD_OFF if selected else "add_subject")
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.row(add_homework_button, add_subject_to_group_button)
    create_group_button = InlineKeyboardButton(text=strings["create_group"] + (" ✅" if selected == "create_group" else ""),
                                               callback_data=KEYBOARD_OFF if selected else "create_group")
    help_button = InlineKeyboardButton(text=strings["help_button"] + (" ✅" if selected == "help_button" else ""),
                                       callback_data=KEYBOARD_OFF if selected else "help")
    keyboard.add(create_group_button, help_button)
    return keyboard
