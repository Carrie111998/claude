"""FastAPI router exposing OmniRoute agent endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from httpx import HTTPStatusError

from app.omniroute.client import OmniRouteClient
from app.omniroute.schemas import (
    AddAgentRequest,
    AgentResponse,
    CreateAgentRequest,
)
from app.dependencies import get_omniroute_client

router = APIRouter(prefix="/omniroute", tags=["omniroute"])


@router.get("/agents", response_model=list[AgentResponse])
async def list_agents(client: OmniRouteClient = Depends(get_omniroute_client)):
    """List all agents available in OmniRoute."""
    try:
        return await client.list_agents()
    except HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"OmniRoute error: {exc.response.text}",
        )


@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    client: OmniRouteClient = Depends(get_omniroute_client),
):
    """Fetch a single OmniRoute agent by ID."""
    try:
        return await client.get_agent(agent_id)
    except HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"OmniRoute error: {exc.response.text}",
        )


@router.post(
    "/agents/add",
    response_model=AgentResponse,
    status_code=status.HTTP_200_OK,
    summary="Add agent from OmniRoute",
)
async def add_agent_from_omniroute(
    body: AddAgentRequest,
    client: OmniRouteClient = Depends(get_omniroute_client),
):
    """
    Import an existing OmniRoute agent into the local system.

    Fetches agent details from OmniRoute by the supplied ``agent_id`` and
    returns the full agent record so the caller can store or invoke it.
    The optional ``alias`` field lets you assign a local friendly name.
    """
    try:
        agent = await client.get_agent(body.agent_id)
    except HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"OmniRoute error: {exc.response.text}",
        )

    if body.alias:
        agent["alias"] = body.alias

    return agent


@router.post(
    "/agents",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new agent in OmniRoute",
)
async def create_agent(
    body: CreateAgentRequest,
    client: OmniRouteClient = Depends(get_omniroute_client),
):
    """Register a brand-new agent with OmniRoute."""
    try:
        return await client.create_agent(body.model_dump())
    except HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"OmniRoute error: {exc.response.text}",
        )


@router.delete("/agents/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    client: OmniRouteClient = Depends(get_omniroute_client),
):
    """Remove an agent from OmniRoute."""
    try:
        await client.delete_agent(agent_id)
    except HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"OmniRoute error: {exc.response.text}",
        )


@router.get("/models", response_model=list[dict])
async def list_models(client: OmniRouteClient = Depends(get_omniroute_client)):
    """List all available models in OmniRoute."""
    try:
        return await client.list_models()
    except HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"OmniRoute error: {exc.response.text}",
        )
