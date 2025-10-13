import asyncio
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

users = set()

@dp.message(Command('start'))
async def send_hello(message: types.Message):
    await message.answer(f'''Hi, {message.from_user.first_name}! I'm "NN keyboard shop" telegram bot.
Here you can buy the best keyboards from different manufacturers:
WLmouse
Wooting
ATK
and others.
Do you wanna know more?''')
    user_id = message.from_user.id
    users.add(user_id)
    await message.answer("Now you're in users list.")

@dp.message(Command('about'))
async def send_about(message: types.Message):
    await message.answer('''I'm bot of popular "NN keyboard shop". You can ask me questions about different keyboard modals we sell.''')

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

    #print("попа")