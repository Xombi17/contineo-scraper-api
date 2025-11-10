#!/usr/bin/env python3
"""
Initialize Neon PostgreSQL Database for Contineo Scraper
Creates the necessary tables for users, CIE marks, and semester records.
"""

import db_utils_neon as db_utils  # Changed from db_utils_sqlite to db_utils_neon

if __name__ == "__main__":
    print("Initializing Neon PostgreSQL database...")
    db_utils.create_db_and_table_pg()
    print("\nDatabase initialized successfully!")
    print(f"Database: {db_utils.PG_DBNAME}")
    print(f"Host: {db_utils.NEON_DB_URI}")
    print("\nYou can now run 'streamlit run st_main.py' to use the application.")