"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from app.config import Settings

settings = Settings()  # type: ignore[call-arg]

DATABASE_URL = "sqlite:///./agents.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Session:
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
