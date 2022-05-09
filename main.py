import asyncio
import logging
import pyspeedtest

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from Bot_Files.config import load_config
from Bot_Files.utils import broadcatser
from Bot_Files.handlers.admins import admin_router

logger = logging.getLogger(__name__)


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
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    config = load_config(".env")
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    for router in [
        admin_router
        # user_router
    ]:
        dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup(bot, config.tg_bot.admins)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
