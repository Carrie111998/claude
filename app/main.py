"""Application entry point."""

from fastapi import FastAPI
from app.config import Settings
from app.omniroute.router import router as omniroute_router

settings = Settings()  # type: ignore[call-arg]

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(omniroute_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
