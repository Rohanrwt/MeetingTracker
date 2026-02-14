# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                          Browser                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Frontend (Vanilla JS + HTML + CSS)                    │ │
│  │  - index.html (Main UI)                                │ │
│  │  - app.js (Client logic)                               │ │
│  │  - styles.css (Styling)                                │ │
│  └─────────────────┬──────────────────────────────────────┘ │
└────────────────────┼────────────────────────────────────────┘
                     │ HTTP/JSON
                     │
┌────────────────────▼────────────────────────────────────────┐
│              FastAPI Backend (Python)                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  main.py - API Routes                                  │ │
│  │  ├─ POST /api/transcripts  (Process transcript)        │ │
│  │  ├─ GET  /api/tasks        (Get tasks)                 │ │
│  │  ├─ PATCH /api/tasks/{id}  (Update task)               │ │
│  │  ├─ DELETE /api/tasks/{id} (Delete task)               │ │
│  │  ├─ GET  /api/transcripts  (Get history)               │ │
│  │  └─ GET  /status           (Health check)              │ │
│  └───────┬────────────────────────────────────────────────┘ │
│          │                                                   │
│  ┌───────▼────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  schemas.py    │  │  llm.py      │  │  database.py   │  │
│  │  (Validation)  │  │  (OpenAI)    │  │  (DB config)   │  │
│  └────────────────┘  └──────┬───────┘  └───────┬────────┘  │
│                             │                   │           │
│                             │                   │           │
└─────────────────────────────┼───────────────────┼───────────┘
                              │                   │
                  ┌───────────▼──────┐   ┌────────▼─────────┐
                  │   OpenAI API     │   │  SQLite Database │
                  │   (GPT-4o-mini)  │   │  (meeting_tracker│
                  │                  │   │   .db)           │
                  └──────────────────┘   └──────────────────┘
```

## Data Flow

### 1. Processing a Transcript

```
User Input
   │
   ▼
┌─────────────────────────┐
│ Paste transcript        │
│ Click "Extract Items"   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ POST /api/transcripts   │
│ { text: "..." }         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ llm.py                  │
│ extract_action_items()  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ OpenAI API              │
│ GPT-4o-mini             │
│ Response: JSON          │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Parse JSON              │
│ Validate items          │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Save to Database        │
│ - Transcript record     │
│ - Task records          │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Return to Frontend      │
│ { transcript_id, tasks }│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Display tasks in UI     │
│ Update history          │
└─────────────────────────┘
```

### 2. Managing Tasks

```
User Action (Edit/Delete/Complete)
   │
   ▼
┌─────────────────────────┐
│ PATCH /api/tasks/{id}   │
│ or                      │
│ DELETE /api/tasks/{id}  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Validate request        │
│ (Pydantic schemas)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Update/Delete in DB     │
│ (SQLAlchemy ORM)        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Return updated data     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Reload tasks in UI      │
└─────────────────────────┘
```

## Database Schema

```
┌─────────────────────────────────────────┐
│             transcripts                  │
├─────────────────────────────────────────┤
│ id (PK)          INTEGER                 │
│ text             TEXT                    │
│ created_at       DATETIME                │
└──────────────┬──────────────────────────┘
               │
               │ 1:N relationship
               │ (cascade delete)
               │
┌──────────────▼──────────────────────────┐
│               tasks                      │
├─────────────────────────────────────────┤
│ id (PK)          INTEGER                 │
│ transcript_id    INTEGER (FK)            │
│ task             TEXT                    │
│ owner            VARCHAR(255) [nullable] │
│ due_date         VARCHAR(50)  [nullable] │
│ status           VARCHAR(20)  [open/done]│
│ created_at       DATETIME                │
└─────────────────────────────────────────┘
```

## Component Breakdown

### Backend Components

```
app/
├── main.py (270 lines)
│   ├── FastAPI app initialization
│   ├── Route definitions
│   ├── Dependency injection (DB sessions)
│   ├── Error handling
│   └── Static file serving
│
├── models.py (35 lines)
│   ├── Transcript model (SQLAlchemy)
│   └── Task model (SQLAlchemy)
│
├── schemas.py (65 lines)
│   ├── Request schemas (Pydantic)
│   ├── Response schemas (Pydantic)
│   └── Validation rules
│
├── database.py (30 lines)
│   ├── Database engine setup
│   ├── Session factory
│   └── Base class for models
│
└── llm.py (125 lines)
    ├── OpenAI client initialization
    ├── extract_action_items() - Main extraction logic
    ├── JSON parsing & validation
    └── check_llm_health() - Health check
```

### Frontend Components

```
app/
├── templates/
│   └── index.html (60 lines)
│       ├── Header section
│       ├── Transcript input form
│       ├── Tasks display section
│       └── Transcript history section
│
└── static/
    ├── styles.css (420 lines)
    │   ├── CSS variables (colors, spacing)
    │   ├── Layout & responsive design
    │   ├── Component styles (cards, buttons, forms)
    │   └── Media queries
    │
    └── app.js (340 lines)
        ├── State management (currentFilter, allTasks)
        ├── Event listeners (forms, buttons)
        ├── API calls (fetch)
        ├── DOM manipulation
        └── Utility functions (formatDate, escapeHtml)
```

## Request/Response Examples

### Process Transcript

**Request:**
```http
POST /api/transcripts HTTP/1.1
Content-Type: application/json

{
  "text": "John will prepare the sales report by Friday."
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
      "task": "Prepare the sales report",
      "owner": "John",
      "due_date": "2024-02-16",
      "status": "open",
      "created_at": "2024-02-14T10:30:00"
    }
  ]
}
```

### Update Task

**Request:**
```http
PATCH /api/tasks/1 HTTP/1.1
Content-Type: application/json

{
  "status": "done"
}
```

**Response:**
```json
{
  "id": 1,
  "transcript_id": 1,
  "task": "Prepare the sales report",
  "owner": "John",
  "due_date": "2024-02-16",
  "status": "done",
  "created_at": "2024-02-14T10:30:00"
}
```

## Error Handling Flow

```
Request
   │
   ▼
┌─────────────────────────┐
│ Input Validation        │
│ (Pydantic)              │
└───────┬─────────────────┘
        │
        ├─ Invalid ──────────► 422 Validation Error
        │
        ▼ Valid
┌─────────────────────────┐
│ Business Logic          │
└───────┬─────────────────┘
        │
        ├─ Not Found ────────► 404 Not Found
        ├─ LLM Error ────────► 500 Internal Error
        ├─ DB Error ─────────► 500 Internal Error
        │
        ▼ Success
┌─────────────────────────┐
│ Return 200 OK           │
└─────────────────────────┘
```

## Deployment Architecture (Render)

```
┌─────────────────────────────────────────────┐
│              Render Platform                 │
│  ┌───────────────────────────────────────┐  │
│  │  Web Service (Python 3.11)            │  │
│  │  ├─ Build: pip install -r req.txt     │  │
│  │  ├─ Start: uvicorn app.main:app       │  │
│  │  └─ Port: $PORT (auto-assigned)       │  │
│  └───────────────┬───────────────────────┘  │
│                  │                           │
│  ┌───────────────▼───────────────────────┐  │
│  │  Persistent Disk (Optional)           │  │
│  │  Mount: /data                         │  │
│  │  Database: /data/meeting_tracker.db   │  │
│  └───────────────────────────────────────┘  │
│                                              │
│  Environment Variables:                      │
│  - OPENAI_API_KEY=sk-...                    │
│  - DATABASE_URL=sqlite:////data/...         │
└──────────────────┬───────────────────────────┘
                   │
                   │ HTTPS (auto-SSL)
                   │
          ┌────────▼─────────┐
          │   Public URL     │
          │ yourapp.onrender │
          │     .com         │
          └──────────────────┘
```

## Technology Choices Rationale

### FastAPI
- ✅ Async support (future-proof)
- ✅ Auto-generated docs
- ✅ Type safety (Python 3.11+)
- ✅ High performance
- ✅ Great DX

### SQLite
- ✅ Zero config
- ✅ File-based (portable)
- ✅ Perfect for <100k records
- ✅ Easy migration to PostgreSQL
- ✅ Great for MVP

### Vanilla JS
- ✅ No build step
- ✅ Fast load times
- ✅ Simple deployment
- ✅ Easy to understand
- ✅ No framework lock-in

### OpenAI (GPT-4o-mini)
- ✅ Best price/performance
- ✅ JSON mode support
- ✅ Fast response (<2s)
- ✅ Good accuracy
- ✅ Managed service

## Performance Characteristics

### Response Times (Expected)
- **Homepage load:** <100ms
- **Process transcript:** 1-3s (LLM processing)
- **Task CRUD:** <50ms
- **Get tasks:** <20ms
- **Health check:** ~500ms (includes LLM ping)

### Scalability
- **Current:** Single instance, ~10 req/s
- **Database:** SQLite handles ~1k writes/s
- **Bottleneck:** OpenAI API rate limits
- **Scaling:** Move to PostgreSQL, add caching

### Resource Usage
- **Memory:** ~150MB (Python process)
- **CPU:** Minimal (mostly I/O bound)
- **Storage:** ~1KB per transcript + tasks
- **Bandwidth:** ~5KB per request (avg)

## Security Model

```
┌─────────────────────────────────────┐
│ Client (Browser)                    │
│ - XSS protection (escapeHtml)       │
│ - HTTPS only (production)           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ FastAPI Backend                     │
│ - Input validation (Pydantic)       │
│ - SQL injection prevention (ORM)    │
│ - No auth (intentional for MVP)     │
└──────────────┬──────────────────────┘
               │
               ├────────────────────────► OpenAI API
               │                         (Data sent to 3rd party)
               │
               ▼
┌─────────────────────────────────────┐
│ SQLite Database                     │
│ - Local file storage                │
│ - No network exposure               │
└─────────────────────────────────────┘
```

## Monitoring Points

```
/status endpoint returns:
{
  "backend": "ok",      ← Python process running
  "database": "ok",     ← DB connection works
  "llm": "ok"           ← OpenAI API reachable
}

Key metrics to track:
├─ Request rate (requests/min)
├─ Response times (p50, p95, p99)
├─ Error rate (% failed requests)
├─ LLM accuracy (manual review)
└─ API costs ($ per day)
```

## Future Architecture Evolution

### Phase 2: Multi-User
```
+ PostgreSQL (replace SQLite)
+ User authentication (JWT)
+ User-specific data isolation
+ Email notifications
```

### Phase 3: Scale
```
+ Redis caching layer
+ Background job queue (Celery)
+ Horizontal scaling (load balancer)
+ CDN for static files
```

### Phase 4: Advanced Features
```
+ WebSocket for real-time updates
+ Export service (PDF, CSV)
+ Calendar integration
+ Mobile apps (API-first architecture)
```

---

**Current Architecture Status:** ✅ Production-ready for small-scale use (1-100 users)

**Recommended Upgrades for Scale:**
- 100-1k users: Add PostgreSQL, Redis caching
- 1k-10k users: Add load balancer, background jobs
- 10k+ users: Microservices, dedicated AI service
