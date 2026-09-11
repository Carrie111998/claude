"""Application entry point."""

from fastapi import FastAPI
from app.config import Settings
from app.db import init_db
from app.omniroute.router import router as omniroute_router
from app.local_agents_router import router as local_agents_router

settings = Settings()  # type: ignore[call-arg]

# Initialize database
init_db()

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(omniroute_router, prefix="/api/v1")
app.include_router(local_agents_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
