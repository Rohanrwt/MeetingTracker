"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use DATABASE_URL from environment variable (Vercel) or fallback to SQLite (local)
# Use DATABASE_URL from environment variable (Vercel) or fallback to SQLite (local)
# If running in Vercel but DATABASE_URL is missing, use /tmp (writable)
fallback_db = "sqlite:////tmp/meeting_tracker.db" if os.environ.get("VERCEL") else "sqlite:///./meeting_tracker.db"
DATABASE_URL = os.getenv("DATABASE_URL", fallback_db)

# Create engine
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)