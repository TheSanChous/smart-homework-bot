from aiogram import Bot, Dispatcher, executor, types
from message_reducer import reduce
import os


bot = Bot(os.getenv("TELEGRAM_API"))
dp = Dispatcher(bot)


@dp.message_handler()
async def message_handler(message: types.Message):
    await reduce(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
