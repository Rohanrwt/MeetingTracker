# Development Prompts Used

This document contains the prompts designed for the OpenAI integration. 

> **Note:** The current deployment uses a cost-free **Pattern Matching Engine** instead of OpenAI. These prompts are preserved for future use if you decide to upgrade to the AI-powered version by adding an API key.

## Initial Project Setup Prompt

```
You are a senior full-stack engineer.
Build a production-ready but minimal web app called:
"Meeting Action Items Tracker (Mini Workspace)"

Tech stack requirements:
- Backend: FastAPI (Python 3.11+)
- Database: SQLite (using SQLAlchemy)
- LLM: OpenAI API (use structured JSON output)
- Frontend: Simple HTML + minimal JavaScript (no heavy frameworks)
- Single project (backend serves frontend)
- Must be deployable on Render

Functional Requirements:
1. Home Page: Simple UI with textarea to paste meeting transcript
2. LLM Processing: Extract action items in strict JSON format
3. Task Management: View, edit, delete, mark done, filter tasks
4. Transcript History: Show last 5 processed transcripts
5. Status Page: Return JSON health check
6. Error Handling: Handle empty transcripts, LLM failures, etc.

[Full specification provided]
```

## LLM Integration Prompts

### Prompt to OpenAI API (Production)

**System Prompt:**
```
You are an AI assistant that extracts action items from meeting transcripts.

Extract all action items, tasks, and follow-ups mentioned in the transcript.
For each action item, identify:
- task: A clear description of what needs to be done
- owner: The person responsible (use their name if mentioned, otherwise null)
- due_date: The deadline in YYYY-MM-DD format if mentioned, otherwise null

Return ONLY valid JSON array with no additional text or markdown formatting.
```

**User Prompt Template:**
```
Extract action items from this meeting transcript:

{transcript}

Return a JSON array of action items in this exact format:
[
  {
    "task": "string",
    "owner": "string or null",
    "due_date": "YYYY-MM-DD or null"
  }
]
```

### Example Inputs/Outputs (for testing)

**Input Transcript:**
```
Team sync meeting - Feb 14, 2024

Discussed Q1 goals and project timeline.

Action Items:
- John will prepare the sales report by Friday
- Sarah mentioned she'll reach out to the design team this week
- We need to schedule a follow-up meeting next Monday
- Marketing deck needs updating (no owner assigned yet)
```

**Expected Output:**
```json
[
  {
    "task": "Prepare the sales report",
    "owner": "John",
    "due_date": "2024-02-16"
  },
  {
    "task": "Reach out to the design team",
    "owner": "Sarah",
    "due_date": null
  },
  {
    "task": "Schedule follow-up meeting",
    "owner": null,
    "due_date": "2024-02-19"
  },
  {
    "task": "Update marketing deck",
    "owner": null,
    "due_date": null
  }
]
```

## Database Design Prompts

### Schema Design Prompt
```
Design SQLAlchemy models for:
1. Transcripts table: id, text, created_at
2. Tasks table: id, transcript_id (FK), task, owner (nullable), 
   due_date (nullable), status (open/done), created_at

Requirements:
- Use SQLite
- Cascade delete (deleting transcript deletes tasks)
- Use proper relationships
- Index on created_at for sorting
```

## API Design Prompts

### Endpoint Specification Prompt
```
Create FastAPI endpoints:
- POST /api/transcripts: Process transcript, return tasks
- GET /api/tasks?status=open: Get tasks with optional filter
- PATCH /api/tasks/{id}: Update task
- DELETE /api/tasks/{id}: Delete task
- GET /api/transcripts?limit=5: Get recent transcripts
- GET /status: Health check (backend, database, LLM)

Use Pydantic schemas for validation.
Handle all error cases gracefully.
```

## Frontend Design Prompts

### UI/UX Prompt
```
Create minimal, clean UI with:
- Textarea for transcript input
- Process button (show loading state)
- Task list with cards
- Filter buttons (All/Open/Done)
- Edit inline form for tasks
- Delete confirmation
- Transcript history list

Style requirements:
- No frameworks (vanilla JS)
- Clean, modern CSS
- Responsive design
- Clear visual hierarchy
- Accessible (semantic HTML)
```

## Testing Prompts

### Edge Case Identification
```
List edge cases to test:
- Empty transcript
- Transcript with no action items
- Very long transcript (>10k words)
- Special characters in names/dates
- Malformed dates ("next Tuesday")
- Multiple owners for one task
- No owner specified
- Transcript in different languages
```

## Documentation Prompts

### README Generation
```
Write comprehensive README.md with:
- Feature list (implemented/not implemented)
- Setup instructions (local + Render deployment)
- API documentation
- Usage examples
- Troubleshooting guide
- Tech stack overview
```

### AI Documentation Prompt
```
Document AI usage:
- Which LLM and why (GPT-4o-mini rationale)
- What was manually verified
- Known limitations
- Cost considerations
- Monitoring recommendations
- Security considerations
```

## Debugging Prompts (if used during development)

```
Debug JSON parsing errors from OpenAI response:
- Handle responses wrapped in ```json blocks
- Handle responses as objects vs arrays
- Handle different key names (action_items, tasks, items)
- Validate each item has required fields
```

## Optimization Prompts

```
Optimize for production:
- Add proper error messages
- Implement request validation
- Add database connection pooling
- Handle LLM timeouts
- Add retry logic for API calls
- Implement rate limiting
```

## Deployment Prompts

```
Create Render deployment guide:
- Environment variables setup
- Build and start commands
- Database persistence strategy
- Health check configuration
- Auto-deploy from git
```

---

## Notes on Prompt Effectiveness

**What Worked Well:**
- Specific tech stack requirements
- Clear input/output examples
- Structured project requirements
- Explicit "what NOT to implement" list

**What Could Be Improved:**
- More specific UI/UX guidelines initially
- Earlier consideration of error states
- More detailed testing scenarios upfront

**Lessons Learned:**
1. Start with architecture overview before code
2. Provide example data for LLM integration
3. Specify error handling requirements explicitly
4. Include deployment considerations early
5. Document as you go (not after)

---

## Prompt Engineering Tips for Similar Projects

1. **Be Specific About Constraints:**
   - "No authentication" vs "Simple auth"
   - "Minimal UI" vs "Feature-rich dashboard"
   - "Production-ready" vs "Prototype"

2. **Provide Examples:**
   - Sample inputs and expected outputs
   - Visual mockups (if available)
   - Similar projects for reference

3. **Specify Non-Functional Requirements:**
   - Performance expectations
   - Error handling approach
   - Deployment targets
   - Cost constraints

4. **Iterate in Phases:**
   - Phase 1: Core functionality
   - Phase 2: Error handling
   - Phase 3: UI polish
   - Phase 4: Documentation

5. **Document Assumptions:**
   - Target users
   - Usage patterns
   - Scale expectations
   - Maintenance approach
