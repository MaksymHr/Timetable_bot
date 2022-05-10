import logging

from asyncpg import UniqueViolationError

from BotFiles.config import load_config
from BotFiles.database.db_api import UsersModel, GroupsModel
from BotFiles.errors.max_number_of_groups import ReachedMaxNumberGroups


async def add_group(group_id: int, owner_id: int, name: str):
    try:
        group = GroupsModel(chat_id=group_id, owner_id=owner_id, name=name)
        await group.create()

    except Exception:
        pass


async def add_group_to_user(user_id: int, group_id: int):
    user = await UsersModel.get(user_id)
    user_groups = user.groups_id

    config = load_config()

    if user_groups:
        if group_id not in user_groups:
            if len(user_groups) != config.max_groups_per_user:
                user_groups.append(group_id)
            else:
                raise ReachedMaxNumberGroups
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


async def select_group(id: int):
    return await GroupsModel.query.where(GroupsModel.chat_id == id).gino.first()


async def select_user(id: int):
    return await UsersModel.query.where(UsersModel.user_id == id).gino.first()
