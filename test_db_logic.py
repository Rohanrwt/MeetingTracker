import os
import sys

# Simulate Vercel environment with a dummy postgres URL to check engine creation logic
# We use a dummy URL that looks like Neon but won't actually connect, just to test the logic path
os.environ["DATABASE_URL"] = "postgresql://user:pass@host/db?sslmode=require"

# Add current directory to path
sys.path.insert(0, os.path.abspath("."))

try:
    print("Importing database module...")
    from app.database import engine, DATABASE_URL
    print(f"DATABASE_URL used: {DATABASE_URL}")
    print(f"Engine created: {engine}")
    print(f"Engine dialect: {engine.dialect.name}")
    print(f"Pool class: {engine.pool.__class__.__name__}")
    
    # Check if we are using the correct branch
    if "sqlite" in str(engine.url):
        print("FAIL: Still using SQLite despite env var!")
    else:
        print("SUCCESS: Using Postgres engine.")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
