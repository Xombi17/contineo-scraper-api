#!/usr/bin/env python3
"""
Entry point for FastAPI backend
Run with: python run_api.py
Or: uvicorn src.api:app --reload
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
