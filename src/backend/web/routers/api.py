from fastapi import APIRouter, Depends

from backend.web.middlewares.deps import current_tg_user, TelegramUser

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/me")
async def me(user: TelegramUser = Depends(current_tg_user)):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "username": user.username,
    }
