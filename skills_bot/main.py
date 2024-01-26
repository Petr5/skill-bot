from bot import dp, bot

if __name__ == '__main__':
    from aiogram import executor
    from aiogram import types

    from handlers import dp

    executor.start_polling(dp, skip_updates=True)
