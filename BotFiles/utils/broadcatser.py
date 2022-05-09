import asyncio
import logging

from aiogram import Bot
from aiogram import exceptions


async def send_message(bot: Bot, user_id, text: str, disable_notification: bool = False) -> bool:
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        return await send_message(bot, user_id, text)  # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcast(bot, users, text) -> int:
    """
    :return: Count of messages
    """
    count = 0

    for user_id in users:
        try:
            if await send_message(bot, user_id, text):
                count += 1
            await asyncio.sleep(0.05)
        except Exception as err:
            logging.info(f"Trouble: {err} on user_id: {user_id}.")

    logging.info(f"{count} of {len(users)} messages successful sent")

    return count
