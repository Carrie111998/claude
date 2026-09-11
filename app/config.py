"""Application configuration via environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # OmniRoute
    omniroute_base_url: str = "https://omniroute-0lvo.srv1854512.hstgr.cloud/v1"
    omniroute_api_key: str

    # App
    app_title: str = "Claude Agent Service"
    app_version: str = "0.1.0"
    debug: bool = False
