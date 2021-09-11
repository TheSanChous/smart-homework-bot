from aiogram import types

from db import Subjects
from db.Users import UserInfo
from db.Groups import GroupInfo
from db.Homeworks import HomeworkInfo
from strings import strings


def get_user_type_switch_keyboard(selected: str = None):
    keyboard = types.InlineKeyboardMarkup(2)
    student_button = types.InlineKeyboardButton(text=strings["student"] + (" ✅" if selected == "student" else ""),
                                                callback_data="student")
    teacher_button = types.InlineKeyboardButton(text=strings["teacher"] + (" ✅" if selected == "teacher" else ""),
                                                callback_data="teacher")
    keyboard.add(student_button, teacher_button)
    return keyboard


def get_join_or_create_group_keyboard(selected: str = None):
    keyboard = types.InlineKeyboardMarkup(2)
    create_button = types.InlineKeyboardButton(text=strings["create_group"] + (" ✅" if selected == "create" else "")
                                               , callback_data="create_group")
    join_button = types.InlineKeyboardButton(text=strings["join_group"] + (" ✅" if selected == "join" else "")
                                             , callback_data="join_group")
    keyboard.add(create_button, join_button)
    return keyboard


def get_student_menu_keyboard(selected: str = None):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    help_button = types.KeyboardButton("О боте ❓")
    keyboard.add(help_button)
    return keyboard


def get_teacher_menu_keyboard(selected: str = None):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    buttons = [
        types.KeyboardButton("О боте ❓"),
        types.KeyboardButton("Создать новую группу 📔"),
        types.KeyboardButton("Добавить предмет в группу ➕"),
        types.KeyboardButton("Задать домашнее задание группе ➕")
    ]
    keyboard.add(*buttons)
    return keyboard


def get_menu_keyboard(user_type: str, selected: str = None):
    if user_type == "student":
        return get_student_menu_keyboard(selected)
    elif user_type == "teacher":
        return get_teacher_menu_keyboard(selected)


def get_user_groups_keyboard(user: UserInfo, selected: str = None):
    groups = user.groups
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for group in groups:
        group_button = types.InlineKeyboardButton(group.name + (" ✅" if selected == str(group.group_id) else "")
                                                  , callback_data=f"{group.group_id}")
        keyboard.add(group_button)
    keyboard.add(types.InlineKeyboardButton("Отменить" + (" ✅" if selected == "cancel" else ""), callback_data="cancel"))
    return keyboard


def get_enter_subject_description_cancel_keyboard(selected: bool = False):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cancel_button = types.InlineKeyboardButton("Пропустить ✅" if selected else "Пропустить",
                                               callback_data="cancel_enter_subject_description")
    keyboard.add(cancel_button)
    return keyboard


def get_group_subjects_switch_keyboard(group: GroupInfo, selected_id: int = None):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for subject in group.subjects:
        keyboard.add(types.InlineKeyboardButton(subject.name + (" ✅" if selected_id == subject.subject_id else ""),
                                                callback_data=str(subject.subject_id)))
    keyboard.add(types.InlineKeyboardButton("Отменить" + (" ✅" if selected_id == -1 else ""), callback_data="cancel"))
    return keyboard


def get_add_homework_types_keyboard(selected: list, complete: bool = False, homework: HomeworkInfo = None):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    add_photo_button = types.InlineKeyboardButton("Прикрепить фото" + (" ✅" if "photo" in selected else ""),
                                                  callback_data="photo")
    add_text_button = types.InlineKeyboardButton("Добавить текстовое сообщение" + (" ✅" if "text" in selected else ""),
                                                 callback_data="text")
    add_file_button = types.InlineKeyboardButton("Прикрепить файл" + (" ✅" if "file" in selected else ""),
                                                 callback_data="file")
    cancel_button = types.InlineKeyboardButton("Отменить" + (" ✅" if "cancel" in selected else ""),
                                               callback_data="cancel")
    keyboard.add(add_text_button, cancel_button)
    if complete:
        keyboard.add(types.InlineKeyboardButton("Готово!" + (" ✅" if "submit" in selected else ""),
                                                callback_data="submit"))
    return keyboard
