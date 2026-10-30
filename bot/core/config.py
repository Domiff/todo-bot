from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_USER: str
    REDIS_PASSWORD: str

    BASE_URL: str

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    def rabbitmq_url(self):
        return (
            f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}//"
        )

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")


settings = Settings()
