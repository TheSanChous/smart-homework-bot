from aiogram import Bot, Dispatcher, executor, types
from message_reducer import reduce_text_message
from callback_reducer import reduce_callback
import os


bot = Bot(os.getenv("TELEGRAM_API"))
dp = Dispatcher(bot)


@dp.message_handler()
async def message_handler(message: types.Message):
    await reduce_text_message(message)


@dp.callback_query_handler(lambda callback_query: True)
async def callback_handler(callback_query: types.CallbackQuery):
    await reduce_callback(callback_query)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
