from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
import sys
from pathlib import Path


class Settings(BaseSettings):
    MODE: Literal["LOCAL", "DEV", "TEST", "PROD"]
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{str(self.DB_PASS)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    model_config = SettingsConfigDict(env_file=f"{Path(__file__).parent.parent/'.env'}")


settings = Settings()
