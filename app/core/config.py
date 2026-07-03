from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str
    SECRET_KEY: str
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()
