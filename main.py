import defs

defs.load_dotenv()
BOT_TOKEN = defs.os.getenv("BOT_TOKEN")
bot = defs.Bot(token=BOT_TOKEN)
dp = defs.Dispatcher()
BRAND = None
CURRENCY = "KZT"

defs.logging.basicConfig(
    level = defs.logging.INFO,
    filename = "bot.log",
    filemode = "a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@dp.message(defs.Command('start'))
async def send_hello(message: defs.types.Message):
    defs.logging.info(f'Start - User name: {message.from_user.first_name} - ID: {message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    banner = defs.FSInputFile("C:/Users/khajj/OneDrive/Desktop/PM project/banner.jpg")
    await message.answer_photo(banner, caption = f'''<b>Hi, {message.from_user.first_name} ✋! I'm "Hiru shop" telegram bot.
Here you can buy the best devices from different manufacturers:</b>

-WLmouse
-Finalmouse
-ATK
-ESP TIGER
-Scyrox

Do you wanna know more?\n\n<b>***MAIN MENU***</b>''', reply_markup = defs.main_menu(), parse_mode="HTML")



@dp.callback_query(defs.F.data == "currency")
async def change_currency(callback_query: defs.types.CallbackQuery, state: defs.FSMContext):
    try:
        await callback_query.message.delete()
    except Exception:
        pass

    pic = defs.FSInputFile(r"C:\Users\khajj\OneDrive\Desktop\PM project\currency.png")
    await callback_query.message.answer_photo(pic,
        caption = "<b>Enter name of currency except to ISO 4217</b>\n\nP.S.:you can find information about this in internet",
        parse_mode = "HTML")
    await state.set_state(defs.Currency.currency)

@dp.message(defs.Currency.currency)
async def currency(message: defs.types.Message, state: defs.FSMContext):
    try:
        await message.delete()
        await message.delete()
    except Exception:
        pass

    await state.update_data(currency = message.text.upper())
    data = await state.get_data()
    global CURRENCY
    CURRENCY = data["currency"]
    check = await defs.save_price(CURRENCY, 10000)

    if str(check).isdigit():
        await message.answer(f"Currency: {CURRENCY}")
        await send_hello(message)
    else:
        await message.answer(f"Wrong name of currency: {check}\n\nCurrency didn't change")
        await send_hello(message)



@dp.callback_query(defs.F.data == "about bot")
async def about_bot(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'About bot - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    try:
        await callback_query.message.delete()
    except Exception:
        pass

    await callback_query.message.answer('''<b>**ABOUT BOT**</b>
I'm bot of popular "Hiru shop". You can ask me questions about different keyboard modals we sell.
Also you can find our site or see information, price and characteristics of different keyboards and computer mice that we sell.''',
    parse_mode="HTML", reply_markup=defs.main_menu())
    await callback_query.answer()



@dp.callback_query(defs.F.data == "about shop")
async def about_shop(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'About shop - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    try:
        await callback_query.message.delete()
    except Exception:
        pass
    await callback_query.message.answer('''<b>**ABOUT SHOP**</b>
"Hiru shop" is well-known internet shop of different top devices. Did you had this situation:
<b>You need cool, comfortable device to play your lovely video games or work comfortably, but you don't have much money.</b>
We think, everyone saw themselves there. So, our shop is good variant for you.''', parse_mode = "HTML", reply_markup=defs.main_menu())
    await callback_query.answer()



@dp.callback_query(defs.F.data == "brands")
async def brands(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'Brands - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')
    print(callback_query.data)

    try:
        await callback_query.message.delete()
    except Exception:
        pass

    pic = defs.FSInputFile(r"C:\Users\khajj\OneDrive\Desktop\PM project\ChatGPT Image Nov 3, 2025, 02_17_53 PM.png")

    await callback_query.message.answer_photo(pic,
        caption = "<b>Choose a brand:</b>",
        parse_mode="HTML",
        reply_markup=defs.mice_and_keyboards()
    )
    await callback_query.answer()




@dp.callback_query(defs.F.data.in_(["scyrox", "wlmouse", "atk", "finalmouse", "esp tiger"]))
async def devices(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'{callback_query.data} - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')
    print(f"[DEBUG] devices() triggered! data = {callback_query.data}")

    global BRAND

    BRAND = callback_query.data
    try:
        await callback_query.message.delete()
    except Exception:
        pass

    pics = {
        "scyrox": r"C:\Users\khajj\OneDrive\Desktop\PM project\c_Yau5JE_400x400.jpg",
        "wlmouse": r"C:\Users\khajj\OneDrive\Desktop\PM project\wlmouse-logo.webp",
        "atk": r"C:\Users\khajj\OneDrive\Desktop\PM project\images.png",
        "finalmouse": r"C:\Users\khajj\OneDrive\Desktop\PM project\800.webp",
        "esp tiger": r"C:\Users\khajj\OneDrive\Desktop\PM project\ESPTIGER_logo_large.png"
        }

    pic = defs.FSInputFile(pics.get(BRAND))

    await callback_query.message.answer_photo(pic,
        caption = f"<b>**{BRAND.upper()}**</b>",
        parse_mode="HTML",
        reply_markup=defs.list_of_devices(BRAND)
    )
    await callback_query.answer()



@dp.callback_query(defs.F.data == "mice")
async def mice_selection(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'Mice - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    try:
        await callback_query.message.delete()
    except Exception:
        pass

    banners = {
        "wlmouse": r"C:\Users\khajj\OneDrive\Desktop\PM project\WLmouse mouse.jpg",
        "scyrox": r"C:\Users\khajj\OneDrive\Desktop\PM project\SCYROX mouse.jpg",
        "atk": r"C:\Users\khajj\OneDrive\Desktop\PM project\ATK GG.jpg",
        "finalmouse": r"C:\Users\khajj\OneDrive\Desktop\PM project\finalmouse mice.jpg"
    }
    banner = defs.FSInputFile(banners.get(BRAND))
    keyboard = defs.get_mouse_by_brand(BRAND)

    await callback_query.message.answer_photo(banner,
        caption = f"<b>**{BRAND.upper()}**\n*MICE*</b>",
        parse_mode = "HTML",
        reply_markup = keyboard)



@dp.callback_query(defs.F.data == "keyboards")
async def keyboards_selection(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'Keyboards - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    try:
        await callback_query.message.delete()
    except Exception:
        pass
    keyboard = defs.get_keyboard_by_brand(BRAND)
    pics = {"wlmouse": r"C:\Users\khajj\OneDrive\Desktop\PM project\WLmouse Keyboard.jpg"}
    pic = defs.FSInputFile(pics.get(BRAND))

    if pic:
        await callback_query.message.answer_photo(pic,
            caption = f"<b>**{BRAND.upper()}**\n*KEYBOARDS*</b>",
            parse_mode="HTML",
            reply_markup=keyboard)
    else:
        defs.logging.error("Error - Wrong repository")



@dp.callback_query(defs.F.data == "mousepads")
async def mousepads_selection(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'Mousepads - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    try:
        await callback_query.message.delete()
    except Exception:
        pass
    keyboard = defs.get_mousepad_by_brand(BRAND)

    pics = {"wlmouse": r"C:\Users\khajj\OneDrive\Desktop\PM project\WLmouse mousepad.jpg"}
    pic = defs.FSInputFile(pics.get(BRAND))

    if pic:
        await callback_query.message.answer_photo(pic,
            caption = "<b>**{BRAND.upper()}**\n*MOUSEPADS*</b>",
            parse_mode="HTML",
            reply_markup=keyboard)
    else:
        defs.logging.error("Error - Wrong repository")



@dp.callback_query(defs.F.data.in_(["WLmouse beast X Max", "WLmouse Strider", "ATK Blazing Sky F1", "Scyrox V6", "Finalmouse ULX Prophecy"]))
async def mice(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'{callback_query.data} - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    global BRAND

    try:
        await callback_query.message.delete()
    except Exception:
        pass

    price = await defs.convertation("mouse", CURRENCY, BRAND, callback_query.data)

    text, keyboard = defs.models_of_mouse(callback_query.data, price, CURRENCY)

    if "Something went wrong" in text:
        await callback_query.message.answer(text, reply_markup=keyboard)

    pics = {
        "WLmouse beast X Max" : r"C:\Users\khajj\OneDrive\Desktop\PM project\max-red.webp",
        "WLmouse Strider" : r"C:\Users\khajj\OneDrive\Desktop\PM project\WLmouse Strider.png",
        "ATK Blazing Sky F1" : r"C:\Users\khajj\OneDrive\Desktop\PM project\ATK Blazing Sky F1.webp",
        "Scyrox V6" : r"C:\Users\khajj\OneDrive\Desktop\PM project\V6.png",
        "Finalmouse ULX Prophecy" : r"C:\Users\khajj\OneDrive\Desktop\PM project\tfuewebsite1.webp"}

    pic = defs.FSInputFile(pics.get(callback_query.data))

    if pic and defs.os.path.exists(pics.get(callback_query.data)):
        await callback_query.message.answer_photo(pic,
            caption=f"<b>**{callback_query.data.upper()}**</b>\n{text}",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    else:
        defs.logging.error("Error - Wrong repository")
        await callback_query.message.answer("Error", reply_markup=keyboard)



@dp.callback_query(defs.F.data.in_(["wlmouse ying75"]))
async def keyboards(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'{callback_query.data} - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    global CURRENCY

    try:
        await callback_query.message.delete()
    except Exception:
        pass

    price = await defs.convertation("keyboards", CURRENCY, BRAND, callback_query.data)

    text, keyboard = defs.models_of_keyboards(callback_query.data, price, CURRENCY)
    pics = {
        "wlmouse ying75": r"C:\Users\khajj\OneDrive\Desktop\PM project\25455-26VTN-WLMOUSE-Ying75-Keyboard.webp"
    }

    pic = defs.FSInputFile(pics.get(callback_query.data))

    if pic and defs.os.path.exists(pics.get(callback_query.data)):
        await callback_query.message.answer_photo(pic,
            caption=f"<b>**{callback_query.data.upper()}**</b>\n{text}",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    else:
        defs.logging.error("Error - Wrong repository")
        await callback_query.message.answer("Error", reply_markup=keyboard)



@dp.callback_query(defs.F.data.in_(["WLmouse Jumi Gaming", "WLmouse Meow Gaming", "ESP TIGER PIONEER Wu Xiang"]))
async def mousepads(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'{callback_query.data} - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    global CURRENCY

    try:
        await callback_query.message.delete()
    except Exception:
        pass
    try:
        price = await defs.convertation("mousepad", CURRENCY, BRAND, callback_query.data)
    except Exception as e:
        await callback_query.message.answer(f"Error: {e}")
        return

    text, keyboard = defs.models_of_mousepad(callback_query.data, price, CURRENCY)

    pics = {
        "WLmouse Jumi Gaming": r"C:\Users\khajj\OneDrive\Desktop\PM project\wlmouse_jumi_gaming_mouse_pad_ac91240_97896.webp",
        "WLmouse Meow Gaming": r"C:\Users\khajj\OneDrive\Desktop\PM project\2_939f53bb-82f8-4b68-bbf1-71a0a1956101.webp",
        "ESP TIGER PIONEER Wu Xiang": r"C:\Users\khajj\OneDrive\Desktop\PM project\ESPTIGER_PIONEER_WUXIANG_WATER_RESISTANCE_GAMING_MOUSEPAD_1.webp"
    }

    print(f"callback_query.data = '{callback_query.data}'")
    print(f"Available keys = {list(pics.keys())}")

    pic = defs.FSInputFile(pics.get(callback_query.data))
    if pic and defs.os.path.exists(pics.get(callback_query.data)):
        await callback_query.message.answer_photo(pic,
            caption=f"<b>**{callback_query.data.upper()}**</b>\n{text}",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    else:
        await callback_query.message.answer("Error", reply_markup=keyboard)



@dp.callback_query(defs.F.data == "back_to_menu")
async def back_to_menu(callback_query: defs.types.CallbackQuery):
    defs.logging.info(f'Back to menu - User name: {callback_query.from_user.first_name} - ID: {callback_query.message.from_user.id} - Time: {defs.datetime.now().strftime("%H:%M:%S")}')

    try:
        await callback_query.message.delete()
    except Exception:
        pass
    await send_hello(callback_query.message)




@dp.error()
async def global_error_handler(error: defs.ErrorEvent):
    # Логируем полный traceback (самое важное)
    defs.logging.error(
        f"Exception caught:\n{error.exception}"
    )

    if isinstance(error.exception, defs.TelegramAPIError):
        defs.logging.error(f"Telegram error: {error.exception}")
        try:
            await error.update.message.answer(
                f"<b>Telegram error⚠️</b>: {error.exception}",
                parse_mode="HTML"
            )
        except Exception:
            await error.update.callback_query.message.answer(
                f"<b>Telegram error⚠️</b>: {error.exception}",
                parse_mode="HTML"
            )
    else:
        try:
            defs.logging.error(f"Something went wrong: {error.exception}")
            await error.update.message.answer(
                "<b>Something went wrong⚙️...Try again later⏳</b>",
                parse_mode="HTML"
            )
        except Exception:
            await error.update.callback_query.message.answer(
                "<b>Something went wrong⚙️...Try again later⏳</b>",
                parse_mode="HTML"
            )


async def main():
    defs.logging.info("Bot started")
    print("Bot activated!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    defs.asyncio.run(main())