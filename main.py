import asyncio
import pyspeedtest

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from TimeTable_bot.config import load_config
from TimeTable_bot.services import broadcatser
from TimeTable_bot.handlers.admins import admin_router


async def on_startup(bot: Bot, admins: list[int]):
    st = pyspeedtest.SpeedTest()
    config = load_config(".env")
    try:
        await broadcatser.broadcast(bot, admins,
                                f"Bot started. "
                                f"Ping to telegram: "
                                f"{round(st.ping(server=f'https://api.telegram.org/bot{config.tg_bot.token}/getMe'), 1)}")
    except Exception as err:
        await broadcatser.broadcast(bot, admins, f"Bot started. Ping to google: "
                                                 f"{round(st.ping(server='google.com'), 1)}")


async def main():
    config = load_config(".env")
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    for router in [
        admin_router
        # user_router,
        # echo_router
    ]:
        dp.include_router(router)

    await on_startup(bot, config.tg_bot.admins)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
