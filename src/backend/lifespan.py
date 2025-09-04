from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from fastapi import FastAPI

from core.config import settings
from backend.bot.handlers import router as handlers_router


def make_lifespan(
    bot: Bot,
    dp: Dispatcher,
    base_url: str,
    webhook_path: str,
    secret_token: str | None,
):
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        dp.include_router(handlers_router)

        webhook_url = base_url.rstrip("/") + webhook_path
        try:
            await bot.set_webhook(
                url=webhook_url,
                secret_token=secret_token or None,
                drop_pending_updates=True,
                allowed_updates=dp.resolve_used_update_types(),
            )
        except Exception:
            # если упали ДО yield — обязательно закрываем сессию
            await bot.session.close()
            raise
        try:
            yield
        finally:
            # сюда попадём только если прошли yield
            try:
                await bot.delete_webhook(drop_pending_updates=False)
            finally:
                await bot.session.close()

    return lifespan
