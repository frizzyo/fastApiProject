from pydantic_settings import BaseSettings, SettingsConfigDict
import sys
from pathlib import Path


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{str(self.DB_PASS)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=f"{Path(__file__).parent.parent/'.env'}")


settings = Settings()
