"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Hardcoded Neon database URL for Vercel deployment
NEON_DATABASE_URL = "postgresql://neondb_owner:npg_wYW4hjMHqF9R@ep-late-credit-aiqtgo22-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Use Neon for Vercel, SQLite for local development
if os.getenv("VERCEL") or os.getenv("VERCEL_ENV"):
    DATABASE_URL = NEON_DATABASE_URL
else:
    DATABASE_URL = "sqlite:///./meeting_tracker.db"

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