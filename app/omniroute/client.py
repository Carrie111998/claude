"""OmniRoute API client for interacting with the OmniRoute platform."""

import httpx
from typing import Any


class OmniRouteClient:
    """Async HTTP client for the OmniRoute API."""

    def __init__(self, base_url: str, api_key: str, timeout: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self._timeout = timeout

    async def list_agents(self) -> list[dict[str, Any]]:
        """Return all agents registered in OmniRoute."""
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(
                f"{self.base_url}/agents",
                headers=self._headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_agent(self, agent_id: str) -> dict[str, Any]:
        """Return a single OmniRoute agent by ID."""
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(
                f"{self.base_url}/agents/{agent_id}",
                headers=self._headers,
            )
            response.raise_for_status()
            return response.json()

    async def create_agent(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Register a new agent in OmniRoute."""
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                f"{self.base_url}/agents",
                headers=self._headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def delete_agent(self, agent_id: str) -> None:
        """Remove an agent from OmniRoute."""
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.delete(
                f"{self.base_url}/agents/{agent_id}",
                headers=self._headers,
            )
            response.raise_for_status()
