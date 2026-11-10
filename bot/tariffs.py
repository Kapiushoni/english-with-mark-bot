from dataclasses import dataclass


@dataclass(frozen=True)
class Tariff:
    code: str
    days: int | None  # None = lifetime
    title: dict[str, str]  # up to 32 chars (Telegram invoice limit)
    description: dict[str, str]  # up to 255 chars


# Prices live in settings (PRICE_MONTH, PRICE_QUARTER, PRICE_LIFETIME in .env).
# To test payments, set a price to 1, pay, and refund the Stars with /refund.
TARIFFS: dict[str, Tariff] = {
    t.code: t
    for t in [
        Tariff(
            code="month",
            days=30,
            title={"uk": "1 місяць доступу", "en": "1 month access"},
            description={
                "uk": "Доступ до закритого каналу English with Mark на 30 днів: уроки, ефіри, домашні завдання.",
                "en": "30 days of access to the private English with Mark channel: lessons, live streams, homework.",
            },
        ),
        Tariff(
            code="quarter",
            days=90,
            title={"uk": "3 місяці доступу", "en": "3 months access"},
            description={
                "uk": "Доступ до закритого каналу на 90 днів. Вигідніше на 20%, ніж помісячно.",
                "en": "90 days of access to the private channel. 20% cheaper than monthly.",
            },
        ),
        Tariff(
            code="lifetime",
            days=None,
            title={"uk": "Доступ назавжди", "en": "Lifetime access"},
            description={
                "uk": "Безстроковий доступ до закритого каналу та всіх майбутніх уроків.",
                "en": "Lifetime access to the private channel and all future lessons.",
            },
        ),
    ]
}
