"""Project configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Project settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    HOST: str = "127.0.0.1"
    PROTOCOL: str = "http"
    APP_NAME: str = "VacancyAggregatorAPI"
    DATABASE_URL: str
    JWT_KEY: str
    PROFILE_PICTURE_DIRECTORY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    HH_CLIENT_ID: str
    HH_CLIENT_SECRET: str
    HH_ACCESS_TOKEN: str


@lru_cache()
def get_settings():
    """Get project settings."""
    return Settings()
