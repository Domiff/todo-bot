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


urls_dict = {
    "base_url": f"{settings.BASE_URL}",
    "read": f"{Urls.READ}",
    "create": f"{Urls.CREATE}",
    "update": f"{Urls.UPDATE}",
    "delete": f"{Urls.DELETE}",
    "register": f"{Urls.REGISTER}",
    "refresh": f"{Urls.REFRESH}",
}
