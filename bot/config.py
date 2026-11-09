from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки читаются из переменных окружения или файла .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str
    # ID закрытого канала, начинается с -100... (0 = ещё не настроен)
    channel_id: int = 0
    # ID администраторов через запятую: 123456789,987654321
    admin_ids_raw: str = Field(default="", alias="ADMIN_IDS")
    database_url: str = "sqlite+aiosqlite:///./data/bot.db"
    support_username: str = "your_support_username"
    check_interval_minutes: int = 10

    @property
    def admin_ids(self) -> set[int]:
        return {int(x) for x in self.admin_ids_raw.replace(" ", "").split(",") if x}
