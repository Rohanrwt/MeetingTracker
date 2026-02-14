"""Main FastAPI application."""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import List
import os

from app.database import get_db, init_db
from app.models import Transcript, Task
from app.schemas import (
    TranscriptCreate,
    TranscriptResponse,
    TaskResponse,
    TaskUpdate,
    ProcessTranscriptResponse,
    StatusResponse
)
from app.llm import extract_action_items, check_llm_health

# Initialize FastAPI app
app = FastAPI(
    title="Meeting Action Items Tracker",
    description="Extract and manage action items from meeting transcripts",
    version="1.0.0"
)

# Mount static files and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database tables on startup."""
    try:
        init_db()
    except Exception as e:
        print(f"Database initialization failed: {e}")
        # Continue anyway, let requests fail if DB is down


# HTML Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the home page."""
    return templates.TemplateResponse("index.html", {"request": request})


# API Routes
@app.post("/api/transcripts", response_model=ProcessTranscriptResponse)
async def process_transcript(
    transcript_data: TranscriptCreate,
    db: Session = Depends(get_db)
):
    """
    Process a meeting transcript and extract action items.
    
    Args:
        transcript_data: The transcript text
        db: Database session
        
    Returns:
        Transcript ID and extracted tasks
        
    Raises:
        HTTPException: If transcript is empty or LLM processing fails
    """
    # Validate transcript is not empty
    if not transcript_data.text.strip():
        raise HTTPException(status_code=400, detail="Transcript cannot be empty")

    try:
        # Extract action items using LLM
        action_items = extract_action_items(transcript_data.text)

        # Save transcript to database
        transcript = Transcript(text=transcript_data.text)
        db.add(transcript)
        db.commit()
        db.refresh(transcript)

        # Save tasks to database
        tasks = []
        for item in action_items:
            task = Task(
                transcript_id=transcript.id,
                task=item["task"],
                owner=item["owner"],
                due_date=item["due_date"],
                status="open"
            )
            db.add(task)
            tasks.append(task)

        db.commit()

        # Refresh tasks to get IDs
        for task in tasks:
            db.refresh(task)

        # Convert to response schema
        task_responses = [TaskResponse.model_validate(task) for task in tasks]

        return ProcessTranscriptResponse(
            transcript_id=transcript.id,
            tasks=task_responses
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process transcript: {str(e)}")


@app.get("/api/tasks", response_model=List[TaskResponse])
async def get_tasks(
    status: str = None,
    db: Session = Depends(get_db)
):
    """
    Get all tasks with optional status filter.
    
    Args:
        status: Filter by status (open/done)
        db: Database session
        
    Returns:
        List of tasks
    """
    query = db.query(Task)
    
    if status:
        if status not in ["open", "done"]:
            raise HTTPException(status_code=400, detail="Status must be 'open' or 'done'")
        query = query.filter(Task.status == status)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    return [TaskResponse.model_validate(task) for task in tasks]


@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get a specific task by ID.
    
    Args:
        task_id: Task ID
        db: Database session
        
    Returns:
        Task details
        
    Raises:
        HTTPException: If task not found
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.model_validate(task)


@app.patch("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a task.
    
    Args:
        task_id: Task ID
        task_update: Fields to update
        db: Database session
        
    Returns:
        Updated task
        
    Raises:
        HTTPException: If task not found
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields if provided
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return TaskResponse.model_validate(task)


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task.
    
    Args:
        task_id: Task ID
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If task not found
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


@app.get("/api/transcripts", response_model=List[TranscriptResponse])
async def get_transcripts(limit: int = 5, db: Session = Depends(get_db)):
    """
    Get recent transcripts with their tasks.
    
    Args:
        limit: Number of transcripts to return (default 5)
        db: Database session
        
    Returns:
        List of transcripts with tasks
    """
    transcripts = db.query(Transcript).order_by(
        Transcript.created_at.desc()
    ).limit(limit).all()
    
    return [TranscriptResponse.model_validate(t) for t in transcripts]


@app.get("/status", response_model=StatusResponse)
async def status_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.
    
    Args:
        db: Database session
        
    Returns:
        Status of backend, database, and LLM services
    """
    # Check backend
    backend_status = "ok"

    # Check database
    database_status = "ok"
    try:
        db.execute("SELECT 1")
    except Exception:
        database_status = "error"

    # Check LLM
    llm_status = "ok"
    if not os.getenv("OPENAI_API_KEY"):
        llm_status = "error: API key not set"
    else:
        try:
            if not check_llm_health():
                llm_status = "error"
        except Exception as e:
            llm_status = f"error: {str(e)}"

    return StatusResponse(
        backend=backend_status,
        database=database_status,
        llm=llm_status
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

app = app  # Vercel needs this