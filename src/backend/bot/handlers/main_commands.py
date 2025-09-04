from aiogram import types, Router, F
from aiogram.filters import CommandStart

from backend.bot.markups import main_kb

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет! Это демо-магазин в Telegram Mini App.\n"
        "Нажми кнопку ниже, чтобы открыть приложение.",
        reply_markup=main_kb,
    )


# 2) Приём данных из Mini App (если ты будешь вызывать tg.sendData(...))
@router.message(F.web_app_data)
async def webapp_data(m: types.Message):
    await m.answer(f"✅ Данные из Mini App:\n<code>{m.web_app_data.data}</code>")
