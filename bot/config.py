from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings are read from environment variables or the .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str
    # Private channel ID, starts with -100... (0 = not configured yet)
    channel_id: int = 0
    # Comma-separated admin IDs: 123456789,987654321
    admin_ids_raw: str = Field(default="", alias="ADMIN_IDS")
    database_url: str = "sqlite+aiosqlite:///./data/bot.db"
    support_username: str = "your_support_username"
    check_interval_minutes: int = 10

    # Plan prices in Telegram Stars (minimum 1)
    price_month: int = Field(default=250, ge=1)
    price_quarter: int = Field(default=600, ge=1)
    price_lifetime: int = Field(default=1500, ge=1)

    @property
    def admin_ids(self) -> set[int]:
        return {int(x) for x in self.admin_ids_raw.replace(" ", "").split(",") if x}

    @property
    def prices(self) -> dict[str, int]:
        """Price in Stars by tariff code."""
        return {"month": self.price_month, "quarter": self.price_quarter, "lifetime": self.price_lifetime}
