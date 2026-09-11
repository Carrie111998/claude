"""SQLAlchemy models for persisting agent data."""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON
from app.db import Base


class LocalAgent(Base):
    """Locally stored agent record."""

    __tablename__ = "agents"

    id = Column(String, primary_key=True, index=True)
    omniroute_id = Column(String, nullable=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    endpoint_url = Column(String)
    alias = Column(String, nullable=True, index=True)
    capabilities = Column(JSON, default=list)
    agent_metadata = Column(JSON, default=dict)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
