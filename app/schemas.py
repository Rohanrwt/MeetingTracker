"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TaskBase(BaseModel):
    """Base task schema."""
    task: str
    owner: Optional[str] = None
    due_date: Optional[str] = None  # YYYY-MM-DD format


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    task: Optional[str] = None
    owner: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(open|done)$")


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: int
    transcript_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class TranscriptCreate(BaseModel):
    """Schema for creating a transcript."""
    text: str = Field(..., min_length=1)


class TranscriptResponse(BaseModel):
    """Schema for transcript response."""
    id: int
    text: str
    created_at: datetime
    tasks: List[TaskResponse] = []

    class Config:
        from_attributes = True


class ProcessTranscriptResponse(BaseModel):
    """Schema for process transcript response."""
    transcript_id: int
    tasks: List[TaskResponse]


class StatusResponse(BaseModel):
    """Schema for status endpoint response."""
    backend: str
    database: str
    llm: str
