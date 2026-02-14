"""SQLAlchemy ORM models."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Transcript(Base):
    """Transcript model - stores meeting transcripts."""
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to tasks
    tasks = relationship("Task", back_populates="transcript", cascade="all, delete-orphan")


class Task(Base):
    """Task model - stores action items extracted from transcripts."""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    transcript_id = Column(Integer, ForeignKey("transcripts.id"), nullable=False)
    task = Column(Text, nullable=False)
    owner = Column(String(255), nullable=True)
    due_date = Column(String(50), nullable=True)  # Store as string in YYYY-MM-DD format
    status = Column(String(20), default="open", nullable=False)  # "open" or "done"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to transcript
    transcript = relationship("Transcript", back_populates="tasks")
