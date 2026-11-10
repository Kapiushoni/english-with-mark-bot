from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.tariffs import TARIFFS
from bot.texts import t


class MenuCB(CallbackData, prefix="m"):
    action: str  # tariffs | my_sub | about | support | lang | back | link | renew


class TariffCB(CallbackData, prefix="t"):
    code: str


class LangCB(CallbackData, prefix="l"):
    code: str


def lang_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t("uk", "btn_lang_uk"), callback_data=LangCB(code="uk"))
    kb.button(text=t("en", "btn_lang_en"), callback_data=LangCB(code="en"))
    kb.adjust(2)
    return kb.as_markup()


def main_menu_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t(lang, "btn_tariffs"), callback_data=MenuCB(action="tariffs"))
    kb.button(text=t(lang, "btn_my_sub"), callback_data=MenuCB(action="my_sub"))
    kb.button(text=t(lang, "btn_about"), callback_data=MenuCB(action="about"))
    kb.button(text=t(lang, "btn_support"), callback_data=MenuCB(action="support"))
    kb.button(text=t(lang, "btn_lang"), callback_data=MenuCB(action="lang"))
    kb.adjust(1, 2, 2)
    return kb.as_markup()


def tariffs_kb(lang: str, prices: dict[str, int]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for tariff in TARIFFS.values():
        kb.button(
            text=t(lang, "tariff_button", title=tariff.title[lang], stars=prices[tariff.code]),
            callback_data=TariffCB(code=tariff.code),
        )
    kb.button(text=t(lang, "btn_back"), callback_data=MenuCB(action="back"))
    kb.adjust(1)
    return kb.as_markup()


def back_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t(lang, "btn_back"), callback_data=MenuCB(action="back"))
    return kb.as_markup()


def my_sub_kb(lang: str, active: bool, lifetime: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if active:
        kb.button(text=t(lang, "btn_get_link"), callback_data=MenuCB(action="link"))
    if not lifetime:
        kb.button(text=t(lang, "btn_renew"), callback_data=MenuCB(action="tariffs"))
    kb.button(text=t(lang, "btn_back"), callback_data=MenuCB(action="back"))
    kb.adjust(1)
    return kb.as_markup()


def renew_kb(lang: str) -> InlineKeyboardMarkup:
    """Button in notifications (reminder, expiry): plans are sent as a new message."""
    kb = InlineKeyboardBuilder()
    kb.button(text=t(lang, "btn_renew"), callback_data=MenuCB(action="renew"))
    return kb.as_markup()
