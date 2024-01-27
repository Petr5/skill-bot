import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from instaloader import instaloader
from PIL import Image
from aiogram.methods.send_photo import SendPhoto
# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")
INSTAGRAM_ACCOUNT = "petr.mavzovin"
# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
bot = Bot(token=TOKEN)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")




def sanitize_filename(filename):
    # Заменяем недопустимые символы в имени файла
    return "".join(c if c.isalnum() or c in "_-" else "_" for c in filename)

@dp.message(lambda message: message.text.startswith("/download_post")) # TODO need to download random post by link
async def download_post_handler(message: types.Message) -> None:
    try:
        # Extract the Instagram account name from the command text
        command_args = message.text.split()
        if len(command_args) < 2:
            await message.reply("Please specify the Instagram account name after the command.")
            return

        instagram_account = command_args[1]

        # Initialize instaloader
        L = instaloader.Instaloader()

        # Download the profile info
        profile = instaloader.Profile.from_username(L.context, instagram_account)

        # Download the most recent post
        for post in profile.get_posts():
            # Download the post
            L.download_post(post, target=instagram_account)

            # Format the date and time
            formatted_datetime = post.date_utc.strftime("%Y-%m-%d_%H-%M-%S_UTC")

            # Create the file path
            file_path = f"{instagram_account}/{formatted_datetime}.jpg"
            file = open(file_path)
            image = Image.open(file_path)

            # Display the image
            image.show()

            await bot.send_photo(chat_id=message.from_user.id, photo=FSInputFile(file_path))

            break  # Exit the loop after the first post

    except Exception as e:
        await message.reply(f"An error occurred: {e}")
async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())