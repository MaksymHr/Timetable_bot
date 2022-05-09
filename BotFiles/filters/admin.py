from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

# from BotFiles.config import Config
from BotFiles.config import load_config

config = load_config(".env")


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message) -> bool:
        return (obj.from_user.id in config.tg_bot.admins) == self.is_admin
