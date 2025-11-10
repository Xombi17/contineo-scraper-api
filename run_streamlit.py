#!/usr/bin/env python3
"""
Entry point for Streamlit app
Run with: python run_streamlit.py
Or: streamlit run src/st_main.py
"""

import sys
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    subprocess.run(["streamlit", "run", "src/st_main.py"])
