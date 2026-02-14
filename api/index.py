import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Force Postgres
os.environ["VERCEL"] = "1"

try:
    from mangum import Mangum
    from app.main import app
    
    # Mangum handler for Vercel
    handler = Mangum(app, lifespan="off")

except Exception as e:
    import traceback
    error_trace = traceback.format_exc()
    print(f"CRASH ON STARTUP: {e}")
    print(error_trace)
    
    # Fallback handler to show error in browser
    def handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "text/plain"},
            "body": f"Startup Error:\n{error_trace}"
        }