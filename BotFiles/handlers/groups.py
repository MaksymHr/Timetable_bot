from aiogram import Router, types
from aiogram.dispatcher.filters.command import CommandStart

from BotFiles.database.gino_commands import add_group, add_group_to_user
from BotFiles.filters.group import IsGroup

group_router = Router()
group_router.message.filter(IsGroup())


@group_router.message(CommandStart())
async def start_chat(msg: types.Message):
    await add_group(
        msg.chat.id,
        msg.from_user.id,
        msg.chat.title
    )

    await add_group_to_user(msg.from_user.id, msg.chat.id)

    await msg.answer(f"Group henlo")

