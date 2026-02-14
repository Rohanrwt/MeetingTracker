import sys
import os

# Add the project root to the python path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app
# Vercel will automatically detect the 'app' variable and serve it
from app.main import app

# Force Vercel env var just in case
os.environ["VERCEL"] = "1"