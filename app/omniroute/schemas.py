"""Pydantic models for OmniRoute request/response payloads."""

from typing import Any
from pydantic import BaseModel, Field


class AgentCapability(BaseModel):
    name: str
    description: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)


class AddAgentRequest(BaseModel):
    """Payload for importing an existing OmniRoute agent by ID."""

    agent_id: str = Field(..., description="OmniRoute agent ID to import")
    alias: str | None = Field(None, description="Local alias for this agent")


class CreateAgentRequest(BaseModel):
    """Payload for registering a brand-new agent in OmniRoute."""

    name: str = Field(..., description="Display name for the agent")
    description: str | None = None
    endpoint_url: str = Field(..., description="HTTP endpoint the agent listens on")
    capabilities: list[AgentCapability] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    """Unified agent representation returned from OmniRoute."""

    id: str
    name: str
    description: str | None = None
    endpoint_url: str
    capabilities: list[AgentCapability] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    status: str = "active"
    alias: str | None = Field(None, description="Local alias assigned when importing")
