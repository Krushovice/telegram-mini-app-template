from backend.web.factory import create_app
from core.config import settings

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.uvicorn.host,
        port=settings.uvicorn.port,
        reload=True,
    )
