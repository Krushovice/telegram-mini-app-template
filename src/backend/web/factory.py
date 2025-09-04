from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from starlette.middleware.cors import CORSMiddleware

from core.config import settings

from backend.web.lifespan import make_lifespan
from backend.web.routers.webhook import make_webhook_router
from backend.web.routers.front import router as front_router


def create_app() -> FastAPI:
    # 1) Собираем bot/dp
    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # 2) Общие параметры вебхука
    webhook_path = "/tg/webhook"
    secret = settings.web.webhook_header_secret or None

    # 3) FastAPI с вынесенным lifespan
    app = FastAPI(
        lifespan=make_lifespan(
            bot=bot,
            dp=dp,
            base_url=settings.web.base_url,
            webhook_path=webhook_path,
            secret_token=secret,
        )
    )
    # Добавим поддержку CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 4) Роутер, который знает только о dp/bot и пути
    app.include_router(front_router)
    app.include_router(
        make_webhook_router(
            dp=dp,
            bot=bot,
            webhook_path=webhook_path,
            secret_token=secret,
        )
    )
    return app
