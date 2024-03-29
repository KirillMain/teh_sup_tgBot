from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from typing import List


class Settings(BaseSettings):
    bot_token: SecretStr
    admin_ids: list[int]
    chat_id: int
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )

config = Settings()