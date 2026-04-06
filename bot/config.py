from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    BASE_URL: str

    model_config = SettingsConfigDict(env_file="../.env.bot", env_file_encoding="utf-8")


settings = Settings()
