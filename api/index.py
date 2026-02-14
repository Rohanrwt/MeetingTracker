import json

def handler(event, context):
    """
    Minimal zero-dependency handler to verify Vercel runtime.
    """
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": "<h1>DEBUG MODE WORKS</h1><p>Vercel environment is healthy. The issue is in the app dependencies or code.</p>"
    }