# db_utils_neon.py
"""
Neon Database Utilities for Contineo Scraper
Using Neon PostgreSQL with MCP server connection
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import pytz
import os
from typing import Dict, List, Optional, Any
import json

# Database configuration from environment variables
NEON_DB_PASSWORD = os.environ.get("NEON_DB_PASSWORD")
NEON_DB_URI = os.environ.get("NEON_DB_URI", "ep-spring-voice-a1yre8if-pooler.ap-southeast-1.aws.neon.tech")
PG_DBNAME = os.environ.get("PG_DBNAME", "neondb")
PG_USER = os.environ.get("PG_USER", "neondb_owner")

# MCP Server configuration
MCP_SERVER_CONFIG = {
    "mcpServers": {
        "Neon": {
            "url": "https://mcp.neon.tech/mcp",
            "headers": {}
        }
    }
}

DB_NAME_FOR_MESSAGES = "Neon PostgreSQL (Cloud Database)"

def get_db_connection():
    """Establishes a connection to the Neon PostgreSQL database."""
    try:
        connection_string = f"postgresql://{PG_USER}:{NEON_DB_PASSWORD}@{NEON_DB_URI}/{PG_DBNAME}?sslmode=require"
        conn = psycopg2.connect(connection_string, cursor_factory=RealDictCursor)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to {DB_NAME_FOR_MESSAGES} database: {e}")
        return None

def create_db_and_table_pg():
    """Creates the users, cie_marks, and semester_records tables if they don't exist."""
    conn = get_db_connection()
    if not conn:
        print("Skipping table creation due to connection failure.")
        return

    cursor = conn.cursor()
    try:
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                prn TEXT NOT NULL UNIQUE,
                dob_day TEXT NOT NULL,
                dob_month TEXT NOT NULL,
                dob_year TEXT NOT NULL
            )
        ''')
        print("Table 'users' checked/created successfully.")

        # Create cie_marks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cie_marks (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                subject_code TEXT NOT NULL,
                exam_type TEXT NOT NULL,
                marks REAL,
                scraped_at TIMESTAMP WITH TIME ZONE NOT NULL,
                UNIQUE (user_id, subject_code, exam_type),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        print("Table 'cie_marks' for leaderboards checked/created successfully.")

        # Create semester_records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS semester_records (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                semester_number INTEGER NOT NULL,
                semester_name TEXT,
                sgpa REAL,
                total_credits INTEGER,
                academic_year TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (user_id, semester_number),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        print("Table 'semester_records' for CGPA tracking checked/created successfully.")

        conn.commit()
    except psycopg2.Error as e:
        print(f"Error creating tables in {DB_NAME_FOR_MESSAGES}: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def add_user_to_db_pg(first_name, full_name, prn, dob_day, dob_month, dob_year):
    """Adds a new user to the Neon PostgreSQL database."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    sql = '''
        INSERT INTO users (first_name, full_name, prn, dob_day, dob_month, dob_year)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (first_name) DO UPDATE SET
            full_name = EXCLUDED.full_name,
            prn = EXCLUDED.prn,
            dob_day = EXCLUDED.dob_day,
            dob_month = EXCLUDED.dob_month,
            dob_year = EXCLUDED.dob_year
    '''
    try:
        cursor.execute(sql, (first_name.lower().strip(), full_name.strip(), prn.strip(), 
                              dob_day.strip(), dob_month.strip(), dob_year.strip()))
        conn.commit()
        print(f"User '{full_name}' added/updated in the {DB_NAME_FOR_MESSAGES} database.")
        return True
    except psycopg2.IntegrityError as e:
        print(f"Error adding user '{full_name}': PRN '{prn}' or Username '{first_name}' might already exist.")
        conn.rollback() 
        return False
    except psycopg2.Error as e:
        print(f"General error adding user to {DB_NAME_FOR_MESSAGES}: {e}")
        conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_user_from_db_pg(first_name_query):
    """
    Retrieves user details from the Neon PostgreSQL database by first name (case-insensitive).
    Also returns the user's primary key 'id'.
    """
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor()
    sql = '''
        SELECT id, full_name, prn, dob_day, dob_month, dob_year
        FROM users
        WHERE first_name = %s
    '''
    try:
        cursor.execute(sql, (first_name_query.lower().strip(),))
        user_data = cursor.fetchone()
        if user_data:
            return {
                "id": user_data["id"],
                "full_name": user_data["full_name"],
                "prn": user_data["prn"],
                "dob_day": user_data["dob_day"],
                "dob_month": user_data["dob_month"],
                "dob_year": user_data["dob_year"]
            }
        return None
    except psycopg2.Error as e:
        print(f"Error fetching user from {DB_NAME_FOR_MESSAGES}: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_student_marks_in_db_pg(user_id, cie_marks_data, scraped_timestamp):
    """
    Deletes old marks and inserts the latest scraped marks for a user.
    This is an 'upsert' (update/insert) operation.
    """
    if not cie_marks_data:
        print("No CIE marks data provided to update in DB.")
        return False

    conn = get_db_connection()
    if not conn: return False
    
    cursor = conn.cursor()
    try:
        # Delete all existing marks for this user
        delete_sql = "DELETE FROM cie_marks WHERE user_id = %s"
        cursor.execute(delete_sql, (user_id,))
        
        # Prepare and insert the new data
        insert_sql = """
            INSERT INTO cie_marks (user_id, subject_code, exam_type, marks, scraped_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        records_to_insert = []
        # Convert timestamp to datetime with timezone
        if isinstance(scraped_timestamp, datetime):
            if scraped_timestamp.tzinfo is None:
                timestamp_with_tz = scraped_timestamp.replace(tzinfo=pytz.UTC)
            else:
                timestamp_with_tz = scraped_timestamp
        else:
            timestamp_with_tz = datetime.now(pytz.UTC)
        
        for subject_code, marks_dict in cie_marks_data.items():
            for exam_type, mark_value in marks_dict.items():
                # Only insert if mark is a valid number
                if isinstance(mark_value, (int, float)):
                    records_to_insert.append((user_id, subject_code, exam_type, mark_value, timestamp_with_tz))

        if records_to_insert:
            cursor.executemany(insert_sql, records_to_insert)
            print(f"Successfully updated {len(records_to_insert)} mark entries for user_id {user_id}.")
        
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Database error during marks update for user_id {user_id}: {e}")
        conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_subject_leaderboard_pg(subject_code, exam_type, limit=3):
    """
    Retrieves the top students for a given subject and exam type.
    """
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    
    sql = """
        SELECT u.full_name, m.marks
        FROM cie_marks m
        JOIN users u ON m.user_id = u.id
        WHERE m.subject_code = %s AND m.exam_type = %s AND m.marks IS NOT NULL
        ORDER BY m.marks DESC
        LIMIT %s
    """
    try:
        cursor.execute(sql, (subject_code, exam_type, limit))
        leaderboard_data = cursor.fetchall()
        return [(row["full_name"], row["marks"]) for row in leaderboard_data]
    except psycopg2.Error as e:
        print(f"Error fetching leaderboard for {subject_code} - {exam_type}: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_all_users_from_db_pg():
    """Retrieves all registered users from the database for the batch update script."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    sql = '''
        SELECT id, full_name, prn, dob_day, dob_month, dob_year
        FROM users
        ORDER BY first_name
    '''
    try:
        cursor.execute(sql)
        all_users_data = cursor.fetchall()
        users_list = []
        for user_data in all_users_data:
            users_list.append({
                "id": user_data["id"],
                "full_name": user_data["full_name"],
                "prn": user_data["prn"],
                "dob_day": user_data["dob_day"],
                "dob_month": user_data["dob_month"],
                "dob_year": user_data["dob_year"]
            })
        return users_list
    except psycopg2.Error as e:
        print(f"Error fetching all users from {DB_NAME_FOR_MESSAGES}: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# --- NEW FUNCTIONS for CGPA/SGPA Management ---

def save_semester_record_pg(user_id, semester_number, semester_name, sgpa, total_credits, academic_year=None):
    """Save or update a semester record for a user."""
    conn = get_db_connection()
    if not conn: return False
    
    cursor = conn.cursor()
    try:
        # Use ON CONFLICT to handle upsert
        cursor.execute("""
            INSERT INTO semester_records 
            (user_id, semester_number, semester_name, sgpa, total_credits, academic_year)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id, semester_number) 
            DO UPDATE SET
                semester_name = EXCLUDED.semester_name,
                sgpa = EXCLUDED.sgpa,
                total_credits = EXCLUDED.total_credits,
                academic_year = EXCLUDED.academic_year,
                created_at = CURRENT_TIMESTAMP
        """, (user_id, semester_number, semester_name, sgpa, total_credits, academic_year))
        
        conn.commit()
        print(f"Semester {semester_number} record saved/updated for user_id {user_id}.")
        return True
    except psycopg2.Error as e:
        print(f"Error saving semester record: {e}")
        conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_user_semester_records_pg(user_id):
    """Get all semester records for a user."""
    conn = get_db_connection()
    if not conn: return []
    
    cursor = conn.cursor()
    sql = '''
        SELECT semester_number, semester_name, sgpa, total_credits, academic_year, created_at
        FROM semester_records
        WHERE user_id = %s
        ORDER BY semester_number ASC
    '''
    try:
        cursor.execute(sql, (user_id,))
        records = cursor.fetchall()
        semester_list = []
        for record in records:
            semester_list.append({
                "semester_number": record["semester_number"],
                "semester_name": record["semester_name"],
                "sgpa": float(record["sgpa"]) if record["sgpa"] else None,
                "total_credits": record["total_credits"],
                "academic_year": record["academic_year"],
                "created_at": record["created_at"].isoformat() if record["created_at"] else None
            })
        return semester_list
    except psycopg2.Error as e:
        print(f"Error fetching semester records: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_user_current_cie_marks_pg(user_id):
    """Get the most recent CIE marks for a user in the format needed for CGPA calculations."""
    conn = get_db_connection()
    if not conn: return {}
    
    cursor = conn.cursor()
    sql = '''
        SELECT subject_code, exam_type, marks
        FROM cie_marks
        WHERE user_id = %s
        ORDER BY subject_code, exam_type
    '''
    try:
        cursor.execute(sql, (user_id,))
        marks_records = cursor.fetchall()
        
        cie_marks_dict = {}
        for record in marks_records:
            subject_code = record["subject_code"]
            exam_type = record["exam_type"]
            marks = record["marks"]
            
            if subject_code not in cie_marks_dict:
                cie_marks_dict[subject_code] = {}
            cie_marks_dict[subject_code][exam_type] = float(marks) if marks else None
        
        return cie_marks_dict
    except psycopg2.Error as e:
        print(f"Error fetching CIE marks: {e}")
        return {}
    finally:
        if cursor: cursor.close()
        if conn: conn.close()