import psycopg2
import os

# Hardcoded from app/database.py
DB_URL = "postgresql://neondb_owner:npg_wYW4hjMHqF9R@ep-late-credit-aiqtgo22-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

try:
    print(f"Connecting to: {DB_URL.split('@')[1]}") # Print host only for privacy/logs
    conn = psycopg2.connect(DB_URL)
    print("Successfully connected!")
    conn.close()
except Exception as e:
    print("Connection failed:")
    print(e)
