import defs

defs.load_dotenv()
BOT_TOKEN = defs.os.getenv("BOT_TOKEN")
bot = defs.Bot(token=BOT_TOKEN)
dp = defs.Dispatcher()
BRAND = None


@dp.message(defs.Command('start'))
async def send_hello(message: defs.types.Message):
    await message.answer(f'''<b>Hi, {message.from_user.first_name} ✋! I'm "NN device shop" telegram bot.
Here you can buy the best devices from different manufacturers:</b>

-Wooting
-ATK

Do you wanna know more?''', parse_mode="HTML")

    await message.answer("**MAIN MENU**", reply_markup = defs.main_menu())



@dp.callback_query(lambda c: c.data == "about bot")
async def about_bot(callback_query: defs.types.CallbackQuery):
    await callback_query.message.edit_text('''<b>**ABOUT BOT**</b>
I'm bot of popular "NN device shop". You can ask me questions about different keyboard modals we sell.
Also you can find our site or see information, price and characteristics of different keyboards and computer mice that we sell.''',
    parse_mode="HTML", reply_markup=defs.main_menu())
    await callback_query.answer()



@dp.callback_query(lambda c: c.data == "about shop")
async def about_shop(callback_query: defs.types.CallbackQuery):
    await callback_query.message.edit_text('''<b>**ABOUT SHOP**</b>
"NN device shop" is well-known internet shop of different top devices. Did you had this situation:
<b>You need cool, comfortable device to play your lovely video games or work comfortably, but you don't have much money.</b>
We think, everyone saw themselves there. So, our shop is good variant for you.''', parse_mode = "HTML", reply_markup=defs.main_menu())
    await callback_query.answer()



@dp.callback_query(lambda c: c.data == "brands")
async def brands(callback_query: defs.types.CallbackQuery):
    await callback_query.message.edit_text(f'''<b>Brands</b>''', parse_mode="HTML", reply_markup=defs.mice_and_keyboards())
    await callback_query.answer()




@dp.callback_query(lambda c: c.data in ["wooting", "wlmouse", "atk"])
async def devices(callback_query: defs.types.CallbackQuery):
    global BRAND
    if callback_query.data == "wooting":
        BRAND = "wooting"
        await callback_query.message.edit_text("<b>**WOOTING**</b>", parse_mode="HTML", reply_markup=defs.list_of_devices())
        await callback_query.answer()

    elif callback_query.data == "wlmouse":
        BRAND = "wlmouse"
        await callback_query.message.edit_text("<b>**WLMOUSE**</b>", parse_mode="HTML", reply_markup=defs.list_of_devices())
        await callback_query.answer()

    elif callback_query.data == "atk":
        BRAND = "atk"
        await callback_query.message.edit_text("<b>**ATK**</b>", parse_mode="HTML", reply_markup=defs.list_of_devices())
        await callback_query.answer()



@dp.callback_query(lambda c: c.data == "mice")
async def mice(callback_query: defs.types.CallbackQuery):
    keyboard = defs.get_mouse_by_brand(BRAND)
    if BRAND == "wlmouse":
        await callback_query.message.answer("<b>**WLMOUSE**</b>\n<b>*MICE*</b>", parse_mode="HTML", reply_markup=keyboard)
    elif BRAND == "atk":
        await callback_query.message.answer("<b>**ATK**</b>\n<b>*MICE*</b>", parse_mode="HTML", reply_markup=keyboard)
    elif BRAND == "wooting":
        await callback_query.message.answer("<b>**WOOTING**</b>\n<b>*MICE*</b>", parse_mode="HTML", reply_markup=keyboard)



@dp.callback_query(lambda c: c.data == "keyboard")
async def keyboard(callback_query: defs.types.CallbackQuery):
    keyboard = defs.get_keyboard_by_brand(BRAND)
    if BRAND == "wlmouse":
        await callback_query.message.answer("")



@dp.callback_query(lambda c: c.data in ["wlmouse_max"])
async def mice(callback_query: defs.types.CallbackQuery):
    model = callback_query.data
    text, keyboard = defs.models_of_mouse(model)
    if callback_query.data == "wlmouse_max":
        model2 = "wlmouse beast max x"
        pic = "https://www.wlmouse.com/cdn/shop/files/max-red.jpg?v=1755482399"

    await callback_query.message.answer_photo(
        photo = pic,
        caption = f"<b>**{model2.upper()}**</b>\n{text}",
        reply_markup=keyboard,
        parse_mode="HTML")



@dp.callback_query(lambda c: c.data == "back")
async def back(callback_query: defs.types.CallbackQuery):
    await callback_query.message.answer("**MAIN MENU**", reply_markup = defs.main_menu())



@dp.error()
async def global_error_handler(error: defs.ErrorEvent):
    if isinstance(error.exception, defs.TelegramAPIError):
        await error.update.message.answer(f"<b>Telegram error⚠️</b>: {error.exception}", parse_mode="HTML")
    else:
        await error.update.message.answer(f"<b>Something went wrong⚙️...Try again later⏳</b>", parse_mode="HTML")


async def main():
    print("Bot activated!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    defs.asyncio.run(main())