import asyncio
import os

from dotenv import load_dotenv
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

users = set()


def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text = "About bot", callback_data = "about bot"), InlineKeyboardButton(text = "About Shop", callback_data = "about shop")],
            [InlineKeyboardButton(text = "Keyboards", callback_data = "keyboard"), InlineKeyboardButton(text = "Mice", callback_data = "mouse")],
            [InlineKeyboardButton(text = "Back", callback_data = "back"), InlineKeyboardButton(text = "Site", url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ")]
        ]
    )



@dp.message(Command('start'))
async def send_hello(message: types.Message):
    await message.answer(f'''<b>Hi, {message.from_user.first_name} ✋! I'm "NN device shop" telegram bot.
Here you can buy the best devices from different manufacturers:</b>

-WLmouse
-Wooting
-ATK

Do you wanna know more?''', parse_mode="HTML")

    await message.answer("**MAIN MENU**", reply_markup = main_menu())

@dp.callback_query(lambda c: c.data == "about bot")
async def about_bot(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('''I'm bot of popular "NN device shop". You can ask me questions about different keyboard modals we sell.
Also you can find our site or see information, price and characteristics of different keyboards and computer mice that we sell.''', reply_markup=main_menu())
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "about shop")
async def about_shop(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('''"NN device shop" is well-known internet shop of different top devices. Did you had this situation:
<b>You need cool, comfortable device to play your lovely video games or work comfortably, but you don't have much money.</b>
We think, everyone saw themselves there. So, our shop is good variant for you.''', parse_mode = "HTML", reply_markup=main_menu())
    await callback_query.answer()


async def main():
    print("Bot activated!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())