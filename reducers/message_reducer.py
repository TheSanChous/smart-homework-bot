from resources.strings import text_commands
from resources.calendar import create_calendar
from scripts import *


async def command_reducer(message: types.Message, user: Users.UserInfo):
    command = message.text[1:].lower()
    if command == "start":
        await try_register_user(message)
    elif command == "menu":
        await send_menu(message, user)
    elif command == "help":
        await send_help(message, user)
    elif command == "about":
        await send_help(message, user)
    elif user.type == "teacher":
        await teacher_command_reducer(message, user)
    elif user.type == "student":
        await student_command_reducer(message, user)
    if command == "calendar":
        await message.answer("dasd", reply_markup=create_calendar())
    pass


async def student_command_reducer(message: types.Message, user: Users.UserInfo):
    command = message.text[1:].lower()


async def teacher_command_reducer(message: types.Message, user: Users.UserInfo):
    command = message.text[1:].lower()
    if command == "create_group":
        await group_create(message, user)
    elif command == "add_homework":
        await add_homework(message, user)
    elif command == "add_subject":
        await add_subject_to_group(message, user)
    pass


async def reduce_message_with_state(message: types.Message, user: Users.UserInfo):
    if message.is_command():
        await message.answer("Сначала, закончите с вопросом выше")
        return
    spl = user.state.split(":")
    state = spl[0]
    args = ':'.join(spl[1:])
    if state == "registration":
        await reduce_registration_state(args, message, user)
    elif state == "group_create":
        await reduce_group_create_state(args, message, user)
    elif state == "add_subject_to_group":
        await reduce_add_subject_to_group_state(args, message, user)
    elif state == "add_homework":
        await reduce_add_homework_state(args, message, user)
    pass


async def reduce_text(message: types.Message, user: Users.UserInfo):
    if message.text.lower() in text_commands["menu"]:
        await send_menu(message, user)
    elif message.text.lower() in text_commands["help"]:
        await send_help(message, user)
    elif user.type == "teacher":
        await teacher_reduce_text(message, user)
    elif user.type == "student":
        await student_reduce_text(message, user)
    else:
        pass


async def teacher_reduce_text(message: types.Message, user: Users.UserInfo):
    if message.text.lower() in text_commands["create_group"]:
        await group_create(message, user)
    elif message.text.lower() in text_commands["add_subject_to_group"]:
        await add_subject_to_group(message, user)
    elif message.text.lower() in text_commands["add_homework"]:
        await add_homework(message, user)
    pass


async def student_reduce_text(message: types.Message, user: Users.UserInfo):
    pass


async def reduce_message_without_state(message: types.Message, user: Users.UserInfo):
    if user.is_registered is False:
        await try_register_user(message)
    elif message.is_command():
        await command_reducer(message, user)
    else:
        await reduce_text(message, user)
    pass


async def reduce_text_message(message: types.Message):
    user = get_user(message.from_user.id)
    if user.state is not None:
        await reduce_message_with_state(message, user)
    else:
        await reduce_message_without_state(message, user)
    pass
