import logging

from aiogram import Router, types
from aiogram.dispatcher.filters.command import CommandStart

from BotFiles.database.gino_commands import add_user

user_router = Router()


@user_router.message(CommandStart())
async def bot_start(msg: types.Message):

    await add_user(
        id=msg.from_user.id,
        name=msg.from_user.full_name,
        username=msg.from_user.username
    )

    await msg.answer("Hello!")