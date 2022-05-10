import logging
from typing import List

from aiogram import Dispatcher
from gino import Gino
import sqlalchemy as sa
from sqlalchemy import Column, DateTime, BigInteger, String, sql, ARRAY, Integer

from BotFiles.config import load_config

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db.func.now())
    updated_at = Column(DateTime(True),
                        default=db.func.now(),
                        onupdate=db.func.now(),
                        server_default=db.func.now())


class UsersModel(TimedBaseModel):
    __tablename__ = "Users"

    user_id = Column(BigInteger, primary_key=True, unique=True)
    name = Column(String)
    username = Column(String)
    groups_id = Column(ARRAY(BigInteger))
    lang = Column(String)

    query: sql.Select


class GroupsModel(TimedBaseModel):
    __tablename__ = "Groups"

    chat_id = Column(BigInteger, primary_key=True, unique=True)
    owner_id = Column(BigInteger)
    name = Column(String)
    link_to_timetable = Column(String)
    number_week = Column(Integer)
    language = Column(String)

    query: sql.Select


async def on_startup(dispatcher: Dispatcher):
    logging.info("Connect to Database")
    config = load_config()
    await db.set_bind(config.db_info.DB_URI)
    # await db.gino.drop_all()
    # await db.gino.create_all()
