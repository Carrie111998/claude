"""FastAPI router for managing locally stored agents."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.services import AgentService
from app.schemas_local import (
    LocalAgentCreate,
    LocalAgentUpdate,
    LocalAgentResponse,
)

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=LocalAgentResponse, status_code=status.HTTP_201_CREATED)
def create_agent(
    agent: LocalAgentCreate,
    db: Session = Depends(get_db),
):
    """Create a new local agent."""
    existing = AgentService.get_agent(db, agent.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Agent with ID {agent.id} already exists",
        )

    db_agent = AgentService.create_agent(db, agent)
    return db_agent


@router.get("", response_model=list[LocalAgentResponse])
def list_agents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """List all locally stored agents."""
    agents = AgentService.list_agents(db, skip=skip, limit=limit)
    return agents


@router.get("/search", response_model=list[LocalAgentResponse])
def search_agents(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Search agents by name, description, or alias."""
    agents = AgentService.search_agents(db, q, skip=skip, limit=limit)
    return agents


@router.get("/{agent_id}", response_model=LocalAgentResponse)
def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific local agent by ID."""
    agent = AgentService.get_agent(db, agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found",
        )
    return agent


@router.put("/{agent_id}", response_model=LocalAgentResponse)
def update_agent(
    agent_id: str,
    update: LocalAgentUpdate,
    db: Session = Depends(get_db),
):
    """Update a local agent."""
    agent = AgentService.update_agent(db, agent_id, update)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found",
        )
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db),
):
    """Delete a local agent."""
    success = AgentService.delete_agent(db, agent_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found",
        )
