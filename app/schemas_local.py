"""Pydantic schemas for local agent storage."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field, ConfigDict


class LocalAgentCreate(BaseModel):
    """Create a local agent record."""

    id: str = Field(..., description="Unique agent ID")
    name: str
    description: str | None = None
    endpoint_url: str
    alias: str | None = None
    capabilities: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    omniroute_id: str | None = None


class LocalAgentUpdate(BaseModel):
    """Update a local agent record."""

    name: str | None = None
    description: str | None = None
    alias: str | None = None
    metadata: dict[str, Any] | None = None


class LocalAgentResponse(BaseModel):
    """Response for a local agent."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    omniroute_id: str | None
    name: str
    description: str | None
    endpoint_url: str
    alias: str | None
    capabilities: list[dict[str, Any]]
    metadata: dict[str, Any] = Field(alias="agent_metadata")
    status: str
    created_at: datetime
    updated_at: datetime
