from enum import StrEnum

from bot.config import settings


class Urls(StrEnum):
    BASE_URL = settings.BASE_URL
    READ = "api/list/"
    CREATE = "api/create/"
    UPDATE = "api/update/"
    DELETE = "api/delete/"
    REGISTER = "auth/tg/register/"
    REFRESH = "auth/token/refresh/"
