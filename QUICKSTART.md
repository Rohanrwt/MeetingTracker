# Quick Start Guide

Get the Meeting Action Items Tracker running in 5 minutes.

## Prerequisites

- Python 3.11+ installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Setup Steps

### 1. Clone & Navigate
```bash
git clone <your-repo-url>
cd meeting-tracker
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate it:
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set API Key
```bash
# On macOS/Linux:
export OPENAI_API_KEY="sk-your-key-here"

# On Windows (PowerShell):
$env:OPENAI_API_KEY="sk-your-key-here"

# Or create a .env file:
cp .env.example .env
# Edit .env and add your API key
```

### 5. Run the App
```bash
python run.py
```

### 6. Open Browser
Navigate to: **http://localhost:8000**

## Quick Test

1. Paste this sample transcript:
   ```
   Team meeting notes - Feb 14, 2024
   
   John will prepare the Q1 sales report by Friday.
   Sarah mentioned she'll review the marketing materials this week.
   We need to schedule a follow-up meeting next Monday.
   ```

2. Click "Extract Action Items"

3. You should see 3 tasks extracted!

## Troubleshooting

**Error: "OPENAI_API_KEY not set"**
- Make sure you've exported the environment variable or created a .env file

**Error: "Module not found"**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

**LLM extraction fails**
- Check your API key is valid
- Verify you have OpenAI API credits
- Check http://localhost:8000/status for health status

**Port already in use**
- Change port in `run.py`: `port=8001`
- Or kill the process using port 8000

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [AI_NOTES.md](AI_NOTES.md) for AI implementation details
- Review [API documentation](http://localhost:8000/docs) (FastAPI auto-generated)

## Deploy to Render

See the "Deployment to Render" section in [README.md](README.md) for detailed instructions.

Quick version:
1. Push code to GitHub
2. Create new Web Service on Render
3. Set `OPENAI_API_KEY` environment variable
4. Deploy!
