import asyncio
import os
from datetime import datetime

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from pydantic_core.core_schema import none_schema

from Prices import devices

import aiohttp
import logging
from dotenv import load_dotenv

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command


from aiogram.types import Message
from aiogram.types import ErrorEvent
from aiogram.exceptions import TelegramAPIError

import math
import json



with open(".idea/devices.json", "r", encoding="utf-8") as file:
        DATA = json.load(file)



class Currency(StatesGroup):
    currency = State()


async def fetch_data(url: str, data_type: str):
    start_time = datetime.now()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    duration = (datetime.now() - start_time).total_seconds()
                    logging.info(f"{data_type} — Успех. Время запроса: {duration} сек.")
                    return data
                else:
                    logging.warning(f"{data_type} — Ошибка: статус {response.status}")
                    return None
    except Exception as e:
        logging.error(f"{data_type} — Ошибка: {e}")
        return None


async def save_price(currency, first_price):
    url = "https://api.fxratesapi.com/latest"
    data = await fetch_data(url, "Convertation")
    try:
        if currency == "USD":
            price = first_price // data["rates"]["KZT"]
        elif currency == "KZT":
            price = first_price
        else:
            price = first_price // data["rates"]["KZT"] * data["rates"][currency]
        return math.ceil(price)
    except Exception as e:
        return str(e)

async def convertation(device, currency, brand, model):
    global DATA
    if device == "keyboards":
        price = await save_price(currency, DATA["Keyboards"][brand][model]["price"])
    elif device == "mouse":
        price = await save_price(currency, DATA["Mice"][brand][model]["price"])
    else:
        price = await save_price(currency, DATA["Mousepads"][brand][model]["price"])
    return price


def get_mice_by_brand(brand):
    buttons = []

    for mouse in DATA["Mice"][brand].keys():
        buttons.append([InlineKeyboardButton(text = f"{mouse}", callback_data=mouse)])

    buttons.append([InlineKeyboardButton(text = f"Back", callback_data="mice"), InlineKeyboardButton(text=f"Back to menu", callback_data="back_to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_keyboards_by_brand(brand):
    buttons = []

    for keyboard in DATA["Keyboards"][brand].keys():
        buttons.append([InlineKeyboardButton(text=f"{keyboard}", callback_data=keyboard)])

    buttons.append([InlineKeyboardButton(text=f"Back", callback_data="keyboards"), InlineKeyboardButton(text=f"Back to menu", callback_data="back_to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_mousepads_by_brand(brand):
    buttons = []

    for mousepad in DATA["Mousepads"][brand].keys():
        buttons.append([InlineKeyboardButton(text=f"{mousepad}", callback_data=mousepad)])

    buttons.append([InlineKeyboardButton(text=f"Back", callback_data="mousepads"), InlineKeyboardButton(text=f"Back to menu", callback_data="back_to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def list_of_devices():
    return InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = "Mice", callback_data="mice")],
        [InlineKeyboardButton(text = "Keyboards", callback_data="keyboards"), InlineKeyboardButton(text = "Mousepads", callback_data="mousepads")],
        [InlineKeyboardButton(text = "Back to menu", callback_data="back_to_menu")],
    ])


def models_of_keyboards(model, price, currency):
    global DATA
    if model == "wlmouse ying75":
        data = DATA["Keyboards"]["wlmouse"]["wlmouse ying75"]["description"]
        text = data.format(price=price, currency=currency)
    elif model == "ATK x ASPAS RS6 Ultra":
        data = DATA["Keyboards"]["atk"]["ATK x ASPAS RS6 Ultra"]["description"]
        text = data.format(price=price, currency=currency)
    elif model == "Rainy 75":
        data = DATA["Keyboards"]["wobkey"]["Rainy 75"]["description"]
        text = data.format(price=price, currency=currency)
    elif model == "Wooting 60HE+":
        data = DATA["Keyboards"]["wooting"]["Wooting 60HE+"]["description"]
        text = data.format(price=price, currency=currency)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")],
        ]
    )
    return text, keyboard


# Выбор модели для мышек
def models_of_mouse(model, price, currency):
    if model == "WLmouse beast X Max":
        data = DATA["Mice"]["wlmouse"]["WLmouse beast X Max"]["description"]
        text = data.format(price=price, currency=currency)

    elif model == "WLmouse Strider":
        data = DATA["Mice"]["wlmouse"]["WLmouse Strider"]["description"]
        text = data.format(price=price, currency=currency)

    elif model == "ATK Blazing Sky F1":
        data = DATA["Mice"]["atk"]["ATK Blazing Sky F1"]["description"]
        text = data.format(price=price, currency=currency)

    elif model == "Scyrox V6":
        data = DATA["Mice"]["scyrox"]["Scyrox V6"]["description"]
        text = data.format(price=price, currency=currency)

    elif model == "Finalmouse ULX Prophecy":
        data = DATA["Mice"]["finalmouse"]["Finalmouse ULX Prophecy"]["description"]
        text = data.format(price=price, currency=currency)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")]
        ]
    )

    return text, keyboard


def models_of_mousepad(model, price, currency):
    if model == "WLmouse Jumi Gaming":
        data = DATA["Mousepads"]["wlmouse"]["WLmouse Jumi Gaming"]["description"]
        text = data.format(price=price, currency=currency)
    elif model == "WLmouse Meow Gaming":
        data = DATA["Mousepads"]["wlmouse"]["WLmouse Meow Gaming"]["description"]
        text = data.format(price=price, currency=currency)
    elif model == "ESPTIGER PIONEER Wu Xiang":
        data = DATA["Mousepads"]["esptiger"]["ESPTIGER PIONEER Wu Xiang"]["description"]
        text = data.format(price=price, currency=currency)
    elif model == "ESPTIGER PIONEER - Ya sheng V2":
        data = DATA["Mousepads"]["esptiger"]["ESPTIGER PIONEER - Ya sheng V2"]["description"]
        text = data.format(price=price, currency=currency)
    elif model == "ESPTIGER PIONEER | Tang Dao":
        data = DATA["Mousepads"]["esptiger"]["ESPTIGER PIONEER | Tang Dao"]["description"]
        text = data.format(price=price, currency=currency)
    elif model == "Olympus Series [Ares]":
        data = DATA["Mousepads"]["evolast gear"]["Olympus Series [Ares]"]["description"]
        text = data.format(price=price, currency=currency)
    elif model == "Wallhack SP-005":
        data = DATA["Mousepads"]["wallhack"]["Wallhack SP-005"]["description"]
        text = data.format(price=price, currency=currency)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")]
        ]
    )
    return text, keyboard


# Выбор "клавиатуры" в зависимости от бренда
def get_mice():
    buttons = []

    for brand in DATA["Mice"].keys():
        buttons.append([InlineKeyboardButton(text = f"{brand.upper()}", callback_data=f"{brand}")])

    buttons.append([InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"),
                    InlineKeyboardButton(text="Back", callback_data='devices')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_keyboard():
    buttons = []

    for brand in DATA["Keyboards"].keys():
        buttons.append([InlineKeyboardButton(text=f"{brand.upper()}", callback_data=f"{brand}")])

    buttons.append([InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"),
                    InlineKeyboardButton(text="Back", callback_data='devices')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_mousepad():
    buttons = []

    for brand in DATA["Mousepads"].keys():
        buttons.append([InlineKeyboardButton(text=f"{brand.upper()}", callback_data=f"{brand}")])

    buttons.append([InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"),
                    InlineKeyboardButton(text="Back", callback_data='devices')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="About bot", callback_data="about bot"),
             InlineKeyboardButton(text="About Shop", callback_data="about shop")],
            [InlineKeyboardButton(text="Devices", callback_data="devices"),
             InlineKeyboardButton(text="Site", url="https://www.instagram.com/reel/DNksxjEtvAv/?igsh=MWQwdHh0eGM2NHg1ag==")],
            [InlineKeyboardButton(text="Change currency", callback_data="currency")],
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")]
        ]
    )