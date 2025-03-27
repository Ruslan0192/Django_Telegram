from loguru import logger
# from notifiers.logging import NotificationHandler

from pydantic_settings import BaseSettings, SettingsConfigDict

# Конфигурирую  logger
LOG_FILE = 'logging/info.json'
logger.add(LOG_FILE,
           format='{extra[telegram_id]} {time} {level} {message}',
           level='INFO',
           rotation='1 month',
           compression='zip',
           colorize=True,
           serialize=True)


class Settings(BaseSettings):
    TOKEN_TG: str
    SHOP_API_TOKEN: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    REDIS_URL: str

    model_config = SettingsConfigDict(env_file=".env_bot")


# Получаем параметры для загрузки переменных среды
settings = Settings()
