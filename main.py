from aiogram import Bot, Dispatcher, types

bot = Bot(token=BOT_TOKEN)

async def send_hello(message: types.Message):
    await message.answer('''Hi! I'm "NN keyboard shop" telegram bot.
Here you can buy the best keyboards from different manufacturers:
WLmouse
Wooting
ATK
and others.
Do you wanna know more?''')
    await message.answer(f"Your first name: {message.from_user.first_name}")

async def send_about(message: types.Message):
    await message.answer('''I'm bot of popular "NN keyboard shop". You can ask me questions about different keyboard modals we sell.''')
if __name__ == '__main__':
