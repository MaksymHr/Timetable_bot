from aiogram import Router, types
from aiogram.dispatcher.filters.command import CommandStart

from BotFiles.database.gino_commands import add_group, add_group_to_user, select_user
from BotFiles.errors.max_number_of_groups import ReachedMaxNumberGroups
from BotFiles.filters.group import IsGroup
from BotFiles.handlers.users import chat_settings

group_router = Router()
group_router.message.filter(IsGroup())


@group_router.message(CommandStart())
async def start_chat(msg: types.Message):
    user = await select_user(msg.from_user.id)

    if user:
        await add_group(
            msg.chat.id,
            msg.from_user.id,
            msg.chat.title
        )

        try:
            await add_group_to_user(msg.from_user.id, msg.chat.id)
            await msg.answer("Бот активирован для этого чата. Перейдите в @timetable_aria_bot для дальнейшей настроки.")

            await chat_settings(msg)

        except ReachedMaxNumberGroups:
            await msg.answer('Бот не активирован. Вы достигли максимального числа чатов (3).')

    else:
        await msg.answer("Сначала необходимо авторизоваться в боте. Перейдите в @timetable_aria_bot и нажмите /start")
