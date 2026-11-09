from dataclasses import dataclass


@dataclass(frozen=True)
class Tariff:
    code: str
    days: int | None  # None = навсегда
    stars: int  # цена в Telegram Stars
    title: dict[str, str]  # до 32 символов (лимит Telegram для счёта)
    description: dict[str, str]  # до 255 символов


# Для теста можно временно поставить stars=1, оплатить и вернуть звёзды командой /refund.
TARIFFS: dict[str, Tariff] = {
    t.code: t
    for t in [
        Tariff(
            code="month",
            days=30,
            stars=250,
            title={"uk": "1 місяць доступу", "en": "1 month access"},
            description={
                "uk": "Доступ до закритого каналу English with Mark на 30 днів: уроки, ефіри, домашні завдання.",
                "en": "30 days of access to the private English with Mark channel: lessons, live streams, homework.",
            },
        ),
        Tariff(
            code="quarter",
            days=90,
            stars=600,
            title={"uk": "3 місяці доступу", "en": "3 months access"},
            description={
                "uk": "Доступ до закритого каналу на 90 днів. Вигідніше на 20%, ніж помісячно.",
                "en": "90 days of access to the private channel. 20% cheaper than monthly.",
            },
        ),
        Tariff(
            code="lifetime",
            days=None,
            stars=1500,
            title={"uk": "Доступ назавжди", "en": "Lifetime access"},
            description={
                "uk": "Безстроковий доступ до закритого каналу та всіх майбутніх уроків.",
                "en": "Lifetime access to the private channel and all future lessons.",
            },
        ),
    ]
}
