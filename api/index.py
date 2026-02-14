import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Force Postgres
os.environ["VERCEL"] = "1"

from mangum import Mangum
from app.main import app
# Database initialization is handled in app.main startup_event

# Mangum handler for Vercel
handler = Mangum(app, lifespan="off")