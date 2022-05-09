import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from BotFiles.config import load_config
from BotFiles.utils import broadcatser
from BotFiles.handlers.admins import admin_router

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, admins: list[int]):
    await broadcatser.broadcast(
        bot,
        admins,
        "Bot started successfully."
    )


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
