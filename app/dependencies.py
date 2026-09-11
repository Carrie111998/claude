"""FastAPI dependency factories."""

from functools import lru_cache

from fastapi import Depends
from app.config import Settings
from app.omniroute.client import OmniRouteClient


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


def get_omniroute_client(
    settings: Settings = Depends(get_settings),
) -> OmniRouteClient:
    return OmniRouteClient(
        base_url=settings.omniroute_base_url,
        api_key=settings.omniroute_api_key,
    )
