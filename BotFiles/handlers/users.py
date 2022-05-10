import logging

from aiogram import Router, types, Bot
from aiogram.dispatcher.filters.command import CommandStart

from BotFiles.config import load_config
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
    # await msg.answer(f"{msg.chat.type}")


@user_router.message(commands=['help'])
async def help_msg(msg: types.Message):
    await msg.answer("Для добавления чата нужно:\n"
                     "1. Добавить бота в чат\n"
                     "2. Если 'Закрепление сообщений' доступно всем - ничего не делать, "
                     "в обратном случае сделать бота администратором и дать соответствующее разрешение\n"
                     "3. Прописать /start@timetable_aria_bot в чате\n"
                     "4. Готово")


async def chat_settings(msg: types.Message):
    config = load_config('.env')
    bot = Bot(token=config.tg_bot.token)
    await bot.send_message(msg.from_user.id, "Settings")

