#!/usr/bin/env python
"""
Script to start the Sentiment Analysis API
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import uvicorn
from api.config import settings

def main():
    """Start the API server"""
    print("🚀 Starting Sentiment Analysis API")
    print(f"📍 Server: http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"📚 Docs: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    print(f"🏥 Health: http://{settings.API_HOST}:{settings.API_PORT}/api/v1/health")
    print("\n✨ Press CTRL+C to stop\n")
    
    uvicorn.run(
        "api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    main()
