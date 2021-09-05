from aiogram import types
from users_repos import user_types
from strings import strings


def get_user_type_switch_keyboard(selected: str = None):
    keyboard = types.InlineKeyboardMarkup(2)
    student_button = types.InlineKeyboardButton(text=strings["student"] + (" ✅" if selected == "student" else ""),
                                                callback_data="student")
    teacher_button = types.InlineKeyboardButton(text=strings["teacher"] + (" ✅" if selected == "teacher" else ""),
                                                callback_data="teacher")
    keyboard.add(student_button, teacher_button)
    return keyboard


def get_join_or_create_group_keyboard():
    keyboard = types.InlineKeyboardMarkup(2)
    create_button = types.InlineKeyboardButton(text=strings["create_group"], callback_data="create_group")
    join_button = types.InlineKeyboardButton(text=strings["join_group"], callback_data="join_group")
    keyboard.add(create_button, join_button)
    return keyboard
