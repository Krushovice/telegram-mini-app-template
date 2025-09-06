from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class BotConfig(BaseModel):
    token: str
    admin: int


class UvicornConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class WebConfig(BaseModel):
    base_url: str
    app_url: str
    webhook_url: str
    webhook_header_secret: str
    webhook_path_secret: str
    # payment_url: str


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool
    echo_pool_size: int
    echo_max_overflow: int


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_prefix="TELEGRAM_APP__",
        env_nested_delimiter="__",
    )

    bot: BotConfig
    web: WebConfig
    uvicorn: UvicornConfig
    db: DatabaseConfig


settings = Settings()
