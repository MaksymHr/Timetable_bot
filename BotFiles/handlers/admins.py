import asyncio
from datetime import datetime
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

    time_start = datetime.now().time()

    ping = 0
    for i in range(0, 60):
        ping += round(st.ping(server="api.telegram.org"), 1)
        await asyncio.sleep(1)
    ping = round(ping / 60, 2)

    time_finish = datetime.now().time()

    await message.edit_text(
        f"Connection test\n"
        f"Start time: {time_start.hour}:{time_start.minute}:{time_start.second}\n"
        f"Finish time: {time_finish.hour}:{time_finish.minute}:{time_finish.second}\n"
        f"Ping: <b>{ping} ms</b>\n"
    )
