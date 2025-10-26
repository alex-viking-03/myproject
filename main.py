import defs

defs.load_dotenv()
BOT_TOKEN = defs.os.getenv("BOT_TOKEN")
bot = defs.Bot(token=BOT_TOKEN)
dp = defs.Dispatcher()
BRAND = None
USER_PATH = {}

defs.logging.basicConfig(
    level = defs.logging.INFO,
    filename = "bot.log",
    filemode = "a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@dp.message(defs.Command('start'))
async def send_hello(message: defs.types.Message):
    defs.logging.info(f'Start - User name: {message.from_user.first_name} - ID: {message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')
    USER_PATH[message.from_user.id] = ["main"]

    await message.answer(f'''<b>Hi, {message.from_user.first_name} ✋! I'm "NN device shop" telegram bot.
Here you can buy the best devices from different manufacturers:</b>

-Wooting
-ATK

Do you wanna know more?''', parse_mode="HTML")

    await message.answer("**MAIN MENU**", reply_markup = defs.main_menu())



@dp.callback_query(lambda c: c.data == "phrase")
async def phrase(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'Back - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    text = await defs.get_phrase()
    keyboard = defs.types.InlineKeyboardMarkup(
        inline_keyboard=[
            [defs.InlineKeyboardButton(text = "🔄Update", callback_data = "phrase")],
            [defs.InlineKeyboardButton(text = "🏠Main menu", callback_data = "back_to_menu")]
        ]
    )
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML", disable_web_page_preview=True)




@dp.callback_query(lambda c: c.data == "about bot")
async def about_bot(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'About bot - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    await callback_query.message.edit_text('''<b>**ABOUT BOT**</b>
I'm bot of popular "NN device shop". You can ask me questions about different keyboard modals we sell.
Also you can find our site or see information, price and characteristics of different keyboards and computer mice that we sell.''',
    parse_mode="HTML", reply_markup=defs.main_menu())
    await callback_query.answer()



@dp.callback_query(lambda c: c.data == "about shop")
async def about_shop(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'About shop - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    await callback_query.message.edit_text('''<b>**ABOUT SHOP**</b>
"NN device shop" is well-known internet shop of different top devices. Did you had this situation:
<b>You need cool, comfortable device to play your lovely video games or work comfortably, but you don't have much money.</b>
We think, everyone saw themselves there. So, our shop is good variant for you.''', parse_mode = "HTML", reply_markup=defs.main_menu())
    await callback_query.answer()



@dp.callback_query(lambda c: c.data == "brands")
async def brands(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'Brands - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    global USER_PATH
    USER_PATH[callback_query.from_user.id].append("brands")

    await callback_query.message.edit_text(f'''<b>***Brands***</b>''', parse_mode="HTML", reply_markup=defs.mice_and_keyboards())
    await callback_query.answer()




@dp.callback_query(lambda c: c.data in ["wooting", "wlmouse", "atk"])
async def devices(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'{callback_query.data} - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    global USER_PATH
    global BRAND
    USER_PATH[callback_query.from_user.id].append(callback_query.data)

    BRAND = callback_query.data
    await callback_query.message.edit_text(f"<b>**{callback_query.data.upper()}**</b>", parse_mode="HTML", reply_markup=defs.list_of_devices())
    await callback_query.answer()



@dp.callback_query(lambda c: c.data == "mice")
async def mice(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'Mice - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')
    global USER_PATH
    USER_PATH[callback_query.from_user.id].append("mice")

    keyboard = defs.get_mouse_by_brand(BRAND)
    USER_PATH[callback_query.from_user.id].append(BRAND)
    await callback_query.message.answer(f"<b>**{BRAND.upper()}**\n*MICE*</b>", parse_mode="HTML", reply_markup=keyboard)



@dp.callback_query(lambda c: c.data == "keyboards")
async def keyboards(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'Keyboards - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')
    global USER_PATH
    USER_PATH[callback_query.from_user.id].append("keyboards")

    keyboard = defs.get_keyboard_by_brand(BRAND)
    USER_PATH[callback_query.from_user.id].append(BRAND)
    await callback_query.message.answer(f"<b>**{BRAND.upper()}**\n*KEYBOARD*</b>", parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data in ["WLmouse beast X Max"])
async def mice(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'{callback_query.data} - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    global USER_PATH
    USER_PATH[callback_query.from_user.id].append(callback_query.data)

    text, keyboard = defs.models_of_mouse(callback_query.data)
    model = callback_query.data
    if model == "WLmouse beast X Max":
        pic = "https://www.wlmouse.com/cdn/shop/files/max-red.jpg?v=1755482399"

    await callback_query.message.answer_photo(
        photo = pic,
        caption = f"<b>**{model.upper()}**</b>\n{text}",
        reply_markup=keyboard,
        parse_mode="HTML")



@dp.callback_query(lambda c: c.data in ["wlmouse ying75"])
async def keyboard(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'{callback_query.data} - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    global USER_PATH
    USER_PATH[callback_query.from_user.id].append("wlmouse_ying75")


    text, keyboard = defs.models_of_keyboards(callback_query.data)
    model = callback_query.data

    if model == "wlmouse ying75":
        pic = "https://mechanicalkeyboards.com/cdn/shop/files/25455-26VTN-WLMOUSE-Ying75-Keyboard.jpg?v=1749633789&width=750"

    await callback_query.message.answer_photo(
        photo = pic,
        caption = f"<b>**{model.upper()}**</b>\n{text}",
        reply_markup=keyboard,
        parse_mode="HTML")



@dp.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback_query: defs.types.CallbackQuery):
    user_id = callback_query.from_user.id
    USER_PATH[user_id] = ["main"]
    defs.logging.info(f'Back to menu - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    await callback_query.message.delete()
    await callback_query.message.answer("**MAIN MENU**", reply_markup = defs.main_menu())



@dp.callback_query(lambda c: c.data == "back")
async def back(callback_query: defs.types.CallbackQuery):
    global USER_PATH
    global BRAND

    defs.logging.info(f'Back - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    user_id = callback_query.from_user.id
    path = USER_PATH.get(user_id, ["main"])

    if len(path) > 1:
        path.pop()
    USER_PATH[user_id] = path

    prev_level = path[-1]

    if prev_level == "main":
        await callback_query.message.answer(text = "<b>**MAIN MENU**</b>", parse_mode = "HTML", reply_markup = defs.main_menu())

    elif prev_level == "brands":
        await brands(callback_query)
        await callback_query.answer()

    elif prev_level in ["wooting", "wlmouse", "atk"]:
        await devices(callback_query)
        await callback_query.answer()

    elif prev_level == "mice":
        await mice(callback_query)
        await callback_query.answer()

    elif prev_level == "keyboards":
        await keyboards(callback_query)
        await callback_query.answer()

    elif prev_level in ["WLmouse beast X Max"]:
        await mice(callback_query)
        await callback_query.answer()

    elif prev_level in ["wlmouse ying75"]:
        await keyboard(callback_query)
        await callback_query.answer()




@dp.error()
async def global_error_handler(error: defs.ErrorEvent):
    if isinstance(error.exception, defs.TelegramAPIError):
        defs.logging.error("Telegram error", error.exception)
        await error.update.message.answer(f"<b>Telegram error⚠️</b>: {error.exception}", parse_mode="HTML")
    else:
        defs.logging.error("Something went wrong", error.exception)
        await error.update.message.answer(f"<b>Something went wrong⚙️...Try again later⏳</b>", parse_mode="HTML")


async def main():
    defs.logging.info("Bot started")
    print("Bot activated!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    defs.asyncio.run(main())