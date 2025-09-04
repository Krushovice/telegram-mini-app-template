from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from core.config import settings

main_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(
        text="🚀 Открыть магазин",
        web_app=WebAppInfo(url=settings.web.base_url)
    )
]])