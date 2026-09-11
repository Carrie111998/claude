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
    endpoint_map = {
        "public": settings.omniroute_base_url,
        "cloudflare": settings.omniroute_cloudflare_url,
        "local": settings.omniroute_local_url,
        "network": settings.omniroute_network_url,
    }
    base_url = endpoint_map.get(settings.omniroute_endpoint, settings.omniroute_base_url)
    return OmniRouteClient(
        base_url=base_url,
        api_key=settings.omniroute_api_key,
    )
