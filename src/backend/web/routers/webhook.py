from fastapi import APIRouter, Request, HTTPException
from aiogram import Bot, Dispatcher
from aiogram.types import Update


def make_webhook_router(
    dp: Dispatcher,
    bot: Bot,
    webhook_path: str,
    secret_token: str | None,
) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    async def health():
        return {"status": "ok"}

    @router.post(webhook_path)
    async def telegram_webhook(request: Request):
        if secret_token:
            got = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
            if got != secret_token:
                raise HTTPException(403, "Bad secret token")
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        return {"ok": True}

    return router
