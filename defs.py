import asyncio
import os
from datetime import datetime

import aiohttp
import logging
from dotenv import load_dotenv
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.types import ErrorEvent
from aiogram.exceptions import TelegramAPIError


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


async def get_phrase():
    url = "https://zenquotes.io/api/random"
    data = await fetch_data(url, "Phrase")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            author = data[0]["a"]
            phrase = data[0]["q"]
            return f'<i>🗨️"{phrase}"</i>\n\n<b>-{author}</b>\n\nSource: {url}'


def get_keyboard_by_brand(brand):
    if brand == "wlmouse":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="YING75 HE Forged Carbon Fiber", callback_data="wlmouse ying75")],
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data="back")],
            ]
        )
    elif brand == "atk":
        pass
    elif brand == "wooting":
        pass


def list_of_devices():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Keyboards", callback_data="keyboards")],
            [InlineKeyboardButton(text="Mice", callback_data="mice")],
            [InlineKeyboardButton(text="Mousepads", callback_data="mousepads")],
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data="back")]
        ]
    )


def models_of_keyboards(model):
    if model == "wlmouse ying75":
        text = ("<b>Price💰:</b> 135000 tenge\n"
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
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")]
            ]
        )
        return text, keyboard


# Выбор модели для мышек
def models_of_mouse(model):
    if model == "WLmouse beast X Max":
        text = ("<b>Price💰:</b> 78000 tenge\n"
                "<b>MCU</b>: Nordic 52840\n"
                "<b>Sensor</b>: PAW3950 HS\n"
                "<b>Polling Rate</b>: 125-8000Hz (Adjustable)\n"
                "<b>Encoder</b>: TTC Dust-Proof silver\n"
                "<b>Switches (Main)</b>: TTC Nihil Transparent Black Dot / Omron Opticals\n"
                "<b>Side Buttons</b>: Omron Blue Dots\n"
                "<b>Battery</b>: Lithium-Ion Polymer 300Mah Capacity\n"
                "<b>Reciever</b>: Nordic 52820,High Speed Chip")
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")]
            ]
        )
        return text, keyboard


# Выбор "клавиатуры" в зависимости от бренда
def get_mouse_by_brand(brand):
    if brand == "wooting":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="version 1.0", callback_data=f"{brand}_1.0")],
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data="back")],
            ]
        )
    elif brand == "atk":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="ATK65", callback_data=f"{brand}_65")],
                [InlineKeyboardButton(text="ATK75", callback_data=f"{brand}_75")],
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data="back")]
            ]
        )
    elif brand == "wlmouse":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="WLmouse beast X Max", callback_data="WLmouse beast X Max")],
                [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data="back")]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="keyboard")]
            ]
        )


# "Клавиатура" для мышек
def mice_and_keyboards():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Wooting", callback_data="wooting")],
            [InlineKeyboardButton(text="WLmouse", callback_data="wlmouse")],
            [InlineKeyboardButton(text="ATK", callback_data="atk")],
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"), InlineKeyboardButton(text="Back", callback_data="back")]
        ]
    )


def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="About bot", callback_data="about bot"),
             InlineKeyboardButton(text="About Shop", callback_data="about shop")],
            [InlineKeyboardButton(text="Brands", callback_data="brands"),
             InlineKeyboardButton(text="Site", url="https://www.instagram.com/reel/DNksxjEtvAv/?igsh=MWQwdHh0eGM2NHg1ag==")],
            [InlineKeyboardButton(text="Get phrase", callback_data="phrase")],
            [InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")]
        ]
    )