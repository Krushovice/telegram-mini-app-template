from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

router = APIRouter()


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
