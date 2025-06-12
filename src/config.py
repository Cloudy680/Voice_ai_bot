# from pydantic_settings import BaseSettings, SettingsConfigDict
#
# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
#
#     TELEGRAM_BOT_TOKEN: str
#     OPENAI_API_KEY: str
#
# settings = Settings()

from pydantic_settings import BaseSettings
from pydantic import Field, ValidationError


class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(..., min_length=1)
    TELEGRAM_BOT_TOKEN: str = Field(..., min_length=1)


    class Config:
        env_file = ".env"


try:
    settings = Settings()
except ValidationError as e:
    raise Exception(f"Ошибка загрузки настроек: {e}") from e