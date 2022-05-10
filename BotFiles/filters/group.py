from aiogram import types
from aiogram.dispatcher.filters import BaseFilter


class IsGroup(BaseFilter):
    async def __call__(self, msg: types.Message) -> bool:
        return msg.chat.type == 'group'
