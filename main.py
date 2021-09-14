from aiogram import Bot, Dispatcher, executor, types
from reducers.message_reducer import reduce_text_message
from reducers.callback_reducer import reduce_callback
from resources.strings import strings
import os


bot = Bot(os.getenv("TELEGRAM_API"))
dp = Dispatcher(bot)

DEBUG = False


@dp.message_handler()
async def message_handler(message: types.Message):
    if DEBUG:
        await message.answer(strings["bot_in_debug"])
    else:
        await reduce_text_message(message)
    pass


@dp.callback_query_handler(lambda callback_query: True)
async def callback_handler(callback_query: types.CallbackQuery):
    if DEBUG:
        await callback_query.message.answer(strings["bot_in_debug"])
    else:
        await reduce_callback(callback_query)
    pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    pass
