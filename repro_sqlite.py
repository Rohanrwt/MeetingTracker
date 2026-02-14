import os
import sys

# Mock LOCAL environment (no VERCEL env var)
if "VERCEL" in os.environ:
    del os.environ["VERCEL"]

# Add current directory to path
sys.path.insert(0, os.path.abspath("."))

try:
    print("Attempting to import app (SQLite mode)...")
    from app.main import app
    print("App imported successfully.")
    
    print("Attempting to initialize DB...")
    from app.database import init_db
    init_db()
    print("DB initialized successfully.")
    
    print("Test passed!")
except Exception as e:
    print(f"Test FAILED: {e}")
    import traceback
    traceback.print_exc()
