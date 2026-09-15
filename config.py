"""
Cau hinh chung cua ung dung (Configuration Layer).
Doc bien moi truong, cung cap gia tri mac dinh cho moi truong demo/local.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Uong Bi GO API"
    DATABASE_URL: str = "sqlite:///./uongbigo.db"

    # JWT
    JWT_SECRET_KEY: str = "uongbigo-super-secret-key-change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 8  # 8 gio

    # Business rules
    CANTEEN_OPEN_HOUR: int = 7    # 7:00
    CANTEEN_CLOSE_HOUR: int = 18  # 18:00
    PAYMENT_TIMEOUT_MINUTES: int = 5  # qua han thi tu dong huy don
    PAYMENT_TIMEOUT_CHECK_INTERVAL_SECONDS: int = 15  # tan suat cronjob quet don het han

    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
