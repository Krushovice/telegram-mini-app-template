from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

router = APIRouter()


@router.get("/")
async def serve_index():
    return FileResponse(FRONTEND_DIR / "index.html")


# статические файлы (css/js/img)
router.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR / "static"),
    name="static",
)
