from fastapi import Header, HTTPException, status

from core.config import settings
from backend.bot.utils.tg_auth import validate_init_data


class TelegramUser:
    def __init__(self, user: dict):
        self.raw = user
        self.id = user.get("id")
        self.first_name = user.get("first_name")
        self.username = user.get("username")


async def current_tg_user(
    x_telegram_init_data: str = Header(default=""),
) -> TelegramUser:
    data = validate_init_data(x_telegram_init_data, settings.bot_token)
    if not data or "user" not in data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram init data",
        )
    # user приходит JSON-строкой, декодируем
    import json

    user = json.loads(data["user"])
    return TelegramUser(user)
