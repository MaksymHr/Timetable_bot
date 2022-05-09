from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admins: list[int]


@dataclass
class DataBaseInfo:
    DB_user: str
    DB_pass: str
    DB_host: str
    DB_port: str
    DB_name: str
    DB_URI: str


@dataclass
class Config:
    tg_bot: TgBot
    db_info: DataBaseInfo


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("TOKEN"),
            admins=list(map(int, env.list("ADMINS")))
        ),
        db_info=DataBaseInfo(
            DB_user=env.str('DB_USER'),
            DB_pass=env.str('DB_PASS'),
            DB_host=env.str('DB_HOST'),
            DB_port=env.str('DB_PORT'),
            DB_name=env.str('DB_NAME'),
            DB_URI=f"postgresql+asyncpg://"
                   f"{env.str('DB_USER')}:{env.str('DB_PASS')}@"
                   f"{env.str('DB_HOST')}:{env.str('DB_PORT')}/{env.str('DB_NAME')}"
        )
    )
