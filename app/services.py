"""Service layer for agent operations."""

from sqlalchemy.orm import Session
from app.models import LocalAgent
from app.schemas_local import LocalAgentCreate, LocalAgentUpdate, LocalAgentResponse


class AgentService:
    """Service for managing local agents."""

    @staticmethod
    def create_agent(db: Session, agent: LocalAgentCreate) -> LocalAgent:
        """Create a new local agent."""
        data = agent.model_dump()
        # Rename metadata to agent_metadata for model
        if "metadata" in data:
            data["agent_metadata"] = data.pop("metadata")
        db_agent = LocalAgent(**data)
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        return db_agent

    @staticmethod
    def get_agent(db: Session, agent_id: str) -> LocalAgent | None:
        """Get a local agent by ID."""
        return db.query(LocalAgent).filter(LocalAgent.id == agent_id).first()

    @staticmethod
    def get_agent_by_omniroute_id(db: Session, omniroute_id: str) -> LocalAgent | None:
        """Get a local agent by OmniRoute ID."""
        return (
            db.query(LocalAgent)
            .filter(LocalAgent.omniroute_id == omniroute_id)
            .first()
        )

    @staticmethod
    def get_agent_by_alias(db: Session, alias: str) -> LocalAgent | None:
        """Get a local agent by alias."""
        return db.query(LocalAgent).filter(LocalAgent.alias == alias).first()

    @staticmethod
    def list_agents(db: Session, skip: int = 0, limit: int = 100) -> list[LocalAgent]:
        """List all local agents with pagination."""
        return db.query(LocalAgent).offset(skip).limit(limit).all()

    @staticmethod
    def update_agent(
        db: Session, agent_id: str, update: LocalAgentUpdate
    ) -> LocalAgent | None:
        """Update a local agent."""
        db_agent = AgentService.get_agent(db, agent_id)
        if not db_agent:
            return None

        update_data = update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_agent, field, value)

        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        return db_agent

    @staticmethod
    def delete_agent(db: Session, agent_id: str) -> bool:
        """Delete a local agent."""
        db_agent = AgentService.get_agent(db, agent_id)
        if not db_agent:
            return False

        db.delete(db_agent)
        db.commit()
        return True

    @staticmethod
    def search_agents(
        db: Session, query: str, skip: int = 0, limit: int = 100
    ) -> list[LocalAgent]:
        """Search agents by name or description."""
        return (
            db.query(LocalAgent)
            .filter(
                (LocalAgent.name.ilike(f"%{query}%"))
                | (LocalAgent.description.ilike(f"%{query}%"))
                | (LocalAgent.alias.ilike(f"%{query}%"))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
