import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import API_TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I am your bot. Type /register to register.")

@dp.message_handler(commands=['register'])
async def register_user(message: types.Message):
    # Assuming you have imported and set up the database session in models.py
    async with AsyncSession() as session:
        username = message.from_user.username
        user = User(username=username)
        session.add(user)
        await session.commit()

    await message.reply(f"User {username} registered successfully!")