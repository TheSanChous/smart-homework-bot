from scripts.add_subject_to_group import *
from scripts.registration import *
from scripts.add_homework import *


async def reduce_callback_with_state(call: types.CallbackQuery, user: Users.UserInfo):
    spl = user.state.split(":")
    state = spl[0]
    args = spl[1]
    if state == "registration":
        await reduce_registration_callback(args, call, user)
    elif state == "add_subject_to_group":
        await reduce_add_subject_to_group_state_callback(args, call, user)
    elif state == "add_homework":
        await reduce_add_homework_state_callback(args, call, user)
    pass


async def reduce_callback(call: types.CallbackQuery):
    user = get_user(call.from_user.id)
    await reduce_callback_with_state(call, user)
