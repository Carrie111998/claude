"""Application configuration via environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # OmniRoute - Multiple endpoints for flexibility
    omniroute_base_url: str = "https://omniroute-0lvo.srv1854512.hstgr.cloud/v1"
    omniroute_cloudflare_url: str = "https://occasions-idol-increasingly-tested.trycloudflare.com/v1"
    omniroute_local_url: str = "http://localhost:32769/v1"
    omniroute_network_url: str = "http://172.16.1.2:20128/v1"
    omniroute_mcp_sse: str = "https://omniroute-0lvo.srv1854512.hstgr.cloud/api/mcp/sse"
    omniroute_endpoint: str = "public"  # Options: public, cloudflare, local, network
    omniroute_api_key: str

    # App
    app_title: str = "Claude Agent Service"
    app_version: str = "0.1.0"
    debug: bool = False
