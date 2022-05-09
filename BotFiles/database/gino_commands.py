from asyncpg import UniqueViolationError

from BotFiles.database.db_api import UsersModel


async def add_user(id: int, name: str, username: str = None):
    try:
        user = UsersModel(user_id=id, name=name, username=username)
        await user.create()

    except UniqueViolationError:
        pass
