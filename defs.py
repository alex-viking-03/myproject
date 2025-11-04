import asyncio
import os
from datetime import datetime

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import Prices

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

    if device == "keyboard":
        price = await save_price(currency, Prices.Keyboards[brand][model])
    elif device == "mouse":
        price = await save_price(currency, Prices.Mice[brand][model])
    else:
        price = await save_price(currency, Prices.Mousepads[brand][model])
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


def list_of_devices():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Keyboards", callback_data="keyboards")],
            [InlineKeyboardButton(text="Mice", callback_data="mice")],
            [InlineKeyboardButton(text="Mousepads", callback_data="mousepads")],
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data="brands")]
        ]
    )


def models_of_keyboards(model, price, currency):
    if model == "wlmouse ying75":
        text = (f"<b>Price💰:</b> {price} {currency}\n"
                "<b>Layout:</b> 75% (84 keys)\n"
                "<b>Material:</b> Forged Carbon\n"
                "<b>Connection:</b> Wired USB Type-C\n"
                "<b>Damping:</b> Poron Sandwich Foam + Poron Bottom Foam\n"
                "<b>Mounting Structure:</b> Gasket-Mounted\n"
                "<b>PCB Plate:</b> Aluminum\n"
                "<b>Lighting:</b> Full RGB Underglow\n"
                "<b>RT Precision:</b> Up to 0.005mm\n"
                "<b>Scan Rate:</b> Full-Key 32K\n"
                "<b>Polling Rate:</b> 125-8000Hz (Customizable), 0.125s Ultra-Low Latency\n"
                "<b>Keycaps:</b> Frosted Transparent PC & Side-Engraved PBT Double-Shot\n"
                "<b>Hot-Swappable HE Switches:</b> Nightfall (Gateron Custom) & Shadow (TTC Custom)")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")],
        ]
    )
    return text, keyboard


# Выбор модели для мышек
def models_of_mouse(model, price, currency):
    if model == "WLmouse beast X Max":
        text = (f"<b>Price💰:</b> {price} {currency}\n"
                "<b>MCU</b>: Nordic 52840\n"
                "<b>Sensor</b>: PAW3950 HS\n"
                "<b>Polling Rate</b>: 125-8000Hz (Adjustable)\n"
                "<b>Encoder</b>: TTC Dust-Proof silver\n"
                "<b>Switches (Main)</b>: TTC Nihil Transparent Black Dot / Omron Opticals\n"
                "<b>Side Buttons</b>: Omron Blue Dots\n"
                "<b>Battery</b>: Lithium-Ion Polymer 300Mah Capacity\n"
                "<b>Reciever</b>: Nordic 52820,High Speed Chip")

    elif model == "WLmouse Strider":
        text = (f"<b>Price💰:</b> {price} {currency}\n"
                "<b>MCU:</b> Nordic 52840\n"
                "<b>Sensor:</b> 3950HS\n"
                "<b>Polling Rate:</b> 125- 8000Hz(Adjustable)\n"
                "<b>DPI:</b> 50-30,000\n"
                "<b>Encoder:</b> TTC Dust-Proof silver\n"
                "<b>LMB/RMB:</b> TTC Nihil Transparent Black Dot / Omron Opticals\n"
                "<b>Side Buttons:</b> Omron Blue Dots\n"
                "<b>Battery:</b> 300mAh")

    elif model == "ATK Blazing Sky F1":
        text = (f"<b>Price💰: </b> {price} {currency}\n"
                "<b>Sensor: </b>PAW3950 / PAW3950 Ultra\n"
                "<b>MCU: </b>Nordic 52840\n"
                "<b>Polling Rate: </b>125-8000Hz (Adjustable)\n"
                "<b>Weight: </b>35g-50g (Varies by Model)\n"
                "<b>Coating: </b>Ice-feeling\n"
                "<b>Dimensions: </b>118.2mm x 62.4mm x 38.8mm")

    elif model == "Scyrox V6":
        text = (f"<b>Price💰: </b> {price} {currency}\n"
                "<b>Connection: </b>Wireless/wired"
                "<b>MCU:</b> Nordic 52840\n"
                "<b>LOD: </b>0.7 - 2.0 mm\n"
                "<b>Weight: </b>40g\n"
                "<b>Sensor: </b>PixArt PAW 3950\n"
                "<b>Switch: </b>Omron Optical\n"               
                "<b>Battery: </b>250mAh\n"
                "<b>Polling Rate: </b>8000 Hz")

    elif model == "Finalmouse ULX Prophecy":
        text = (f"<b>Price💰: </b> {price} {currency}\n"
                "<b>Connection: </b>Wireless/wired"
                "<b>MCU:</b> Nordic 52840\n"
                "<b>Weight: </b>36g\n"  
                "<b>Sensor: </b>PixArt PAW 3395\n"
                "<b>Switch: </b>Transparent Blue Shell Pink Dot\n"               
                "<b>Battery: </b>250mAh\n"
                "<b>Polling Rate: </b>8000 Hz")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")]
        ]
    )

    return text, keyboard


def models_of_mousepad(model, price, currency):
    if model == "WLmouse Jumi Gaming":
        text = (f"<b>Price💰: </b> {price} {currency}\n"
                "<b>Edges</b>: Narrow, ultra-low\n"
                "<b>Base</b>: SlimFlex HR (Previously named Japanese Poron)\n"
                "<b>Hardness</b>: XSoft\n"
                "<b>Type</b>: Speed"
        )
    elif model == "WLmouse Meow Gaming":
        text = (f"<b>Price💰: </b> {price} {currency}\n"
                "<b>Size: </b>490*420*4 mm"
                "<b>Edges: </b>Narrow, ultra-low\n"
                "<b>Base: </b>SlimFlex HR (Previously named Japanese Poron)\n"
                "<b>Hardness: </b>XSoft\n"
                "<b>Type: </b>Speed\n"
        )
    elif model == "ESP TIGER PIONEER Wu Xiang":
        text = (f"<b>Price💰: </b> {price} {currency}\n"
                "<b>Size: </b>480mm x 400mm\n"
                "<b>Thickness: </b>4mm\n"
                "<b>Edge: </b>Durable, Recessed Stitching\n"
                "<b>Base: </b>Anti-Slip Inoac SlimFlex | Poron\n"
                "<b>Surface: </b>NEW Rainbow Pearl Film\n"
                "💦Water-Resistant")
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