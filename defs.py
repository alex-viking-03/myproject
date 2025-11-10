import asyncio
import os
from datetime import datetime

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
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

    if currency == "USD":
        price = first_price // data["rates"]["KZT"]
    elif currency == "RUB":
        price = first_price // data["rates"]["KZT"] * data["rates"]["RUB"]
    elif currency == "KZT":
        price = first_price
    return math.ceil(price)

async def convertation(device, currency, brand, model):
    global DATA
    if device == "keyboards":
        price = await save_price(currency, DATA["Keyboards"][brand][model]["price"])
    elif device == "mouse":
        price = await save_price(currency, DATA["Mice"][brand][model]["price"])
    else:
        price = await save_price(currency, DATA["Mousepads"][brand][model]["price"])
    return price



def get_keyboard_by_brand(brand):
    if brand == "wlmouse":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="YING75 HE Forged Carbon Fiber", callback_data="wlmouse ying75")],
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data=brand)],
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data=brand)],
            ]
        )


def list_of_devices(brand):
    buttons = []

    for category, brands in DATA.items():
        if brand in brands:
            buttons.append([InlineKeyboardButton(text=category.upper(), callback_data=category.lower())])
        else:
            print(f"[DEBUG] ❌ NOT FOUND: {brand} in {category}")

    buttons.append([InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data='brands')])
    return InlineKeyboardMarkup(inline_keyboard = buttons)


def models_of_keyboards(model, price, currency):
    global DATA
    if model == "wlmouse ying75":
        data = DATA["Keyboards"]["wlmouse"]["wlmouse ying75"]["description"]
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

    elif model == "ESP TIGER PIONEER Wu Xiang":
        data = DATA["Mousepads"]["esp tiger"]["ESP TIGER PIONEER Wu Xiang"]["description"]
        text = data.format(price=price, currency=currency)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")]
        ]
    )
    return text, keyboard


# Выбор "клавиатуры" в зависимости от бренда
def get_mouse_by_brand(brand):
    if brand == "scyrox":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Scyrox V6", callback_data="Scyrox V6")],
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data="scyrox")],
            ]
        )
    elif brand == "atk":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="ATK Blazing Sky F1", callback_data=f"ATK Blazing Sky F1")],
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data="atk")]
            ]
        )
    elif brand == "wlmouse":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="WLmouse beast X Max", callback_data="WLmouse beast X Max")],
                [InlineKeyboardButton(text="WLmouse Strider", callback_data="WLmouse Strider")],
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data="wlmouse")]
            ]
        )
    elif brand == "finalmouse":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text = "Finalmouse ULX Prophecy", callback_data="Finalmouse ULX Prophecy")],
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data="finalmouse")]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data=brand)]
            ]
        )


def get_mousepad_by_brand(brand):
    if brand == "wlmouse":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="WLmouse Jumi Gaming", callback_data="WLmouse Jumi Gaming")],
                [InlineKeyboardButton(text="WLmouse Meow Gaming", callback_data="WLmouse Meow Gaming")],
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"),
                 InlineKeyboardButton(text="Back", callback_data="wlmouse")]
            ]
        )
    elif brand == "esp tiger":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="ESP TIGER PIONEER Wu Xiang", callback_data="ESP TIGER PIONEER Wu Xiang")],
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"),
                 InlineKeyboardButton(text="Back", callback_data="finalmouse")]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Back", callback_data=brand)]
            ]
        )


# "Клавиатура" для мышек
def mice_and_keyboards():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Scyrox", callback_data="scyrox"),InlineKeyboardButton(text="WLmouse", callback_data="wlmouse")],
            [InlineKeyboardButton(text="ATK", callback_data="atk"), InlineKeyboardButton(text="Finalmouse", callback_data="finalmouse")],
            [InlineKeyboardButton(text="ESP TIGER", callback_data="esp tiger")],
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")]
        ]
    )


def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="About bot", callback_data="about bot"),
             InlineKeyboardButton(text="About Shop", callback_data="about shop")],
            [InlineKeyboardButton(text="Brands", callback_data="brands"),
             InlineKeyboardButton(text="Site", url="https://www.instagram.com/reel/DNksxjEtvAv/?igsh=MWQwdHh0eGM2NHg1ag==")],
            [InlineKeyboardButton(text="Change currency", callback_data="currency")],
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")]
        ]
    )