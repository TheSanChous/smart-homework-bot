from variables import KEYBOARD_OFF
from scripts import *


async def reduce_callback_with_state(call: types.CallbackQuery, user: Users.UserInfo):
    if call.data == KEYBOARD_OFF:
        await call.answer("Вы уже ответили на этот вопрос.")
        return
    spl = user.state.split(":")
    state = spl[0]
    args = ':'.join(spl[1:])
    if state == "menu":
        await call.message.edit_reply_markup(get_menu_inline_keyboard(selected=call.data))
        await reduce_menu_callback(call, user)
    elif state == "registration":
        await reduce_registration_callback(args, call, user)
    elif state == "add_subject_to_group":
        await reduce_add_subject_to_group_state_callback(args, call, user)
    elif state == "add_homework":
        await reduce_add_homework_state_callback(args, call, user)
    else:
        await call.answer("Вы уже ответили на этот вопрос.")
    pass


async def reduce_callback(call: types.CallbackQuery):
    user = get_user(call.from_user.id)
    print(user.state)
    if user.state is not None:
        await reduce_callback_with_state(call, user)
    else:
        await call.answer("Данное меню уже не активно..")
    pass
