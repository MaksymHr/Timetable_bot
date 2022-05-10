import logging

from asyncpg import UniqueViolationError

from BotFiles.database.db_api import UsersModel, GroupsModel


async def add_group(group_id: int, owner_id: int, name: str):
    try:
        group = GroupsModel(chat_id=group_id, owner_id=owner_id, name=name)
        await group.create()

    except Exception:
        pass


async def add_group_to_user(user_id: int, group_id: int):
    user = await UsersModel.get(user_id)
    user_groups = user.groups_id

    if user_groups:
        if group_id not in user_groups:
            user_groups.append(group_id)
    else:
        user_groups = [group_id]

    await user.update(groups_id=user_groups).apply()


async def add_user(id: int, name: str, username: str = None, ):
    try:
        user = UsersModel(user_id=id, name=name, username=username)
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await UsersModel.query.gino.all()
    return users


async def select_user(id: int):
    user = await UsersModel.query.where(UsersModel.user_id == id).gino.first()
    return user
