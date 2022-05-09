from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admins: list[int]


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("TOKEN"),
            admins=list(map(int, env.list("ADMINS")))
        )
    )
