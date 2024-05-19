import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс для базовых настроек приложения."""

    app_title: str
    database_url: str

    jwt_secret: str = 'secret'
    token_lifetime: int = 3600

    password_min_length: int = 8

    first_superuser_email: str
    first_superuser_password: str

    task_title_min_length: int = 1
    task_title_max_length: int = 255

    logging_format: str = '%(asctime)s - %(levelname)s - %(message)s'

    class Config:
        env_file = '.env'
        extra = 'ignore'


settings = Settings()


def configure_logger(name) -> logging.Logger:
    """Настроить логгер."""

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        settings.logging_format
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
