from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = "8331943625:AAH5J2Ab1RTtKaga_LuSobUjyc3vlBSJZtA"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands = ["start"])
async def send_hello(message: types.Message):
    await message.answer('''Hi! I'm "NN keyboard shop" telegram bot.
Here you can buy the best keyboards from different manufacturers:
WLmouse
Wooting
ATK
and others.
Do you wanna know more?''')
    await message.answer(f"Your first name: {message.from_user.first_name}")

@dp.message_handler(commands = ["about"])
async def send_about(message: types.Message):
    await message.answer('''I'm bot of popular "NN keyboard shop". You can ask me questions about different keyboard modals we sell.''')
if __name__ == '__main__':
