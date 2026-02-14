import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Force Postgres
os.environ["VERCEL"] = "1"

from mangum import Mangum
from app.main import app
from app.database import init_db

# Initialize database
try:
    init_db()
except Exception as e:
    print(f"DB init warning: {e}")

# Mangum handler for Vercel
handler = Mangum(app, lifespan="off")