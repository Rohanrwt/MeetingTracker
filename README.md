# Meeting Action Items Tracker (Mini Workspace)

A production-ready web application that extracts action items from meeting transcripts using AI (OpenAI) and provides a simple interface to manage them.

## Features

✅ **Implemented:**
- Process meeting transcripts and extract action items using OpenAI
- View all action items with filtering (open/done)
- Edit task details (description, owner, due date)
- Mark tasks as done/open
- Delete tasks
- View last 5 processed transcripts
- Health check endpoint (`/status`)
- Clean, minimal UI (no frameworks)
- Production-ready error handling
- SQLite database with SQLAlchemy ORM

❌ **Not Implemented:**
- User authentication/authorization
- Multi-user support
- Task assignments/notifications
- Advanced filtering/search
- Export functionality
- Real-time updates (websockets)
- Task priority levels
- Recurring tasks

## Tech Stack

- **Backend:** FastAPI (Python 3.11+)
- **Database:** SQLite with SQLAlchemy
- **LLM:** OpenAI API (GPT-4o-mini)
- **Frontend:** HTML + Vanilla JavaScript + CSS
- **Deployment:** Render-ready

## Project Structure

```
meeting-tracker/
├── app/
│   ├── main.py           # FastAPI application & routes
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic validation schemas
│   ├── database.py       # Database configuration
│   ├── llm.py            # OpenAI integration
│   ├── templates/
│   │   └── index.html    # Frontend HTML
│   └── static/
│       ├── styles.css    # Styles
│       └── app.js        # Frontend JavaScript
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── AI_NOTES.md          # AI implementation notes
├── PROMPTS_USED.md      # Development prompts
└── ABOUTME.md           # Developer info
```

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd meeting-tracker
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**
   No API key required - uses intelligent pattern matching

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the application:**
   - Open browser: http://localhost:8000
   - API docs: http://localhost:8000/docs
   - Status check: http://localhost:8000/status

## API Endpoints

### POST `/api/transcripts`
Process a meeting transcript and extract action items.

**Request:**
```json
{
  "text": "Team meeting notes here..."
}
```

**Response:**
```json
{
  "transcript_id": 1,
  "tasks": [
    {
      "id": 1,
      "transcript_id": 1,
      "task": "Prepare sales report",
      "owner": "John",
      "due_date": "2024-02-20",
      "status": "open",
      "created_at": "2024-02-14T10:00:00"
    }
  ]
}
```

### GET `/api/tasks`
Get all tasks with optional status filter.

**Query Parameters:**
- `status` (optional): `open` or `done`

### GET `/api/tasks/{task_id}`
Get a specific task by ID.

### PATCH `/api/tasks/{task_id}`
Update a task.

**Request:**
```json
{
  "task": "Updated task description",
  "owner": "Jane",
  "due_date": "2024-02-25",
  "status": "done"
}
```

### DELETE `/api/tasks/{task_id}`
Delete a task.

### GET `/api/transcripts`
Get recent transcripts with their tasks.

**Query Parameters:**
- `limit` (optional, default: 5): Number of transcripts to return

### GET `/status`
Health check endpoint.

**Response:**
```json
{
  "backend": "ok",
  "database": "ok",
  "llm": "ok"
}
```

## Deployment to Render

### Step 1: Prepare Repository
Ensure all files are committed to a Git repository (GitHub, GitLab, etc.)

### Step 2: Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your repository
4. Configure the service:

   **Basic Settings:**
   - Name: `meeting-tracker`
   - Region: Choose closest to your users
   - Branch: `main`
   - Root Directory: (leave blank)
   - Runtime: `Python 3`

   **Build & Deploy:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

   **Environment Variables:**
   - No API key required - uses intelligent pattern matching

   **Instance Type:**
   - Choose "Free" for testing or "Starter" for production

5. Click "Create Web Service"

### Step 3: Database Persistence

Render's free tier has ephemeral file systems. For production:

1. Add a Render Disk:
   - Go to your service settings
   - Click "Disks" → "Add Disk"
   - Mount Path: `/data`
   - Size: 1 GB (or as needed)

2. Update `database.py`:
   ```python
   DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////data/meeting_tracker.db")
   ```

### Step 4: Verify Deployment

Once deployed:
1. Visit your Render URL (e.g., `https://meeting-tracker-xyz.onrender.com`)
2. Check `/status` endpoint to verify all services are operational
3. Test by processing a sample transcript

## Usage Example

1. **Process a transcript:**
   - Paste meeting notes into the textarea
   - Click "Extract Action Items"
   - View extracted tasks below

2. **Manage tasks:**
   - Click "Edit" to modify task details
   - Click "✓ Done" to mark as complete
   - Click "Delete" to remove
   - Use filter buttons to view specific task states

3. **View history:**
   - Scroll to "Recent Transcripts" section
   - See last 5 processed transcripts

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `DATABASE_URL` | No | SQLite database path (default: `sqlite:///./meeting_tracker.db`) |

## Troubleshooting

### LLM errors
- Check `/status` endpoint to verify LLM health
- Ensure you have OpenAI API credits

### Database errors
- Check file permissions in deployment environment
- For Render: ensure disk is properly mounted

### Empty task extraction
- Ensure transcript contains actionable items
- Try more explicit language (e.g., "John will...", "due by Friday")

## Development

### Running tests
```bash
# Add when implementing tests
pytest
```

### Code formatting
```bash
# Recommended tools
black app/
isort app/
```

## License

MIT

## Support

For issues or questions, please open an issue in the repository.
