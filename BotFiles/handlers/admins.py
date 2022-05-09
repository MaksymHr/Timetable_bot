import asyncio
import logging

import pyspeedtest
from aiogram import Router
from aiogram.types import Message

from BotFiles.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(commands=['system'], state=["*"])
async def system_info(msg: Message):
    st = pyspeedtest.SpeedTest()

    message = await msg.answer("Starting measuring ping...")

    ping = 0
    for i in range(0, 10):
        ping += round(st.ping(server="api.telegram.org"), 1)
        await asyncio.sleep(1)
    ping = round(ping / 10, 2)

    try:
        await message.edit_text(
            f"Connection test from 10 sec\n"
            f"Ping: <b>{ping} ms</b>\n"
        )
    except Exception as err:
        logging.error("Cannot connect to check ping.")
