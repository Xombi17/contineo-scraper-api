# db_utils_sqlite.py
"""
SQLite Database Utilities for Contineo Scraper
Local database - no external setup needed!
"""
import sqlite3
from datetime import datetime
import pytz
import os

DB_FILE = "contineo_scraper.db"
DB_NAME_FOR_MESSAGES = "SQLite (Local Database)"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    except sqlite3.Error as e:
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject_code TEXT NOT NULL,
                exam_type TEXT NOT NULL,
                marks REAL,
                scraped_at TEXT NOT NULL,
                UNIQUE (user_id, subject_code, exam_type),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        print("Table 'cie_marks' for leaderboards checked/created successfully.")

        # Create semester_records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS semester_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                semester_number INTEGER NOT NULL,
                semester_name TEXT,
                sgpa REAL,
                total_credits INTEGER,
                academic_year TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (user_id, semester_number),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        print("Table 'semester_records' for CGPA tracking checked/created successfully.")

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating tables in {DB_NAME_FOR_MESSAGES}: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def add_user_to_db_pg(first_name, full_name, prn, dob_day, dob_month, dob_year):
    """Adds a new user to the SQLite database."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    sql = '''
        INSERT INTO users (first_name, full_name, prn, dob_day, dob_month, dob_year)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    try:
        cursor.execute(sql, (first_name.lower().strip(), full_name.strip(), prn.strip(), 
                              dob_day.strip(), dob_month.strip(), dob_year.strip()))
        conn.commit()
        print(f"User '{full_name}' added to the {DB_NAME_FOR_MESSAGES} database.")
        return True
    except sqlite3.IntegrityError: 
        print(f"Error adding user '{full_name}': PRN '{prn}' or Username '{first_name}' might already exist.")
        conn.rollback() 
        return False
    except sqlite3.Error as e:
        print(f"General error adding user to {DB_NAME_FOR_MESSAGES}: {e}")
        conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_user_from_db_pg(first_name_query):
    """
    Retrieves user details from the SQLite database by first name (case-insensitive).
    Also returns the user's primary key 'id'.
    """
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor()
    sql = '''
        SELECT id, full_name, prn, dob_day, dob_month, dob_year
        FROM users
        WHERE first_name = ?
    '''
    try:
        cursor.execute(sql, (first_name_query.lower().strip(),))
        user_data = cursor.fetchone()
        if user_data:
            return {
                "id": user_data[0],
                "full_name": user_data[1],
                "prn": user_data[2],
                "dob_day": user_data[3],
                "dob_month": user_data[4],
                "dob_year": user_data[5]
            }
        return None
    except sqlite3.Error as e:
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
        delete_sql = "DELETE FROM cie_marks WHERE user_id = ?"
        cursor.execute(delete_sql, (user_id,))
        
        # Prepare and insert the new data
        insert_sql = """
            INSERT INTO cie_marks (user_id, subject_code, exam_type, marks, scraped_at)
            VALUES (?, ?, ?, ?, ?)
        """
        records_to_insert = []
        # Convert timestamp to string for SQLite
        timestamp_str = scraped_timestamp.isoformat() if isinstance(scraped_timestamp, datetime) else str(scraped_timestamp)
        
        for subject_code, marks_dict in cie_marks_data.items():
            for exam_type, mark_value in marks_dict.items():
                # Only insert if mark is a valid number
                if isinstance(mark_value, (int, float)):
                    records_to_insert.append((user_id, subject_code, exam_type, mark_value, timestamp_str))

        if records_to_insert:
            cursor.executemany(insert_sql, records_to_insert)
            print(f"Successfully updated {len(records_to_insert)} mark entries for user_id {user_id}.")
        
        conn.commit()
        return True
    except sqlite3.Error as e:
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
        WHERE m.subject_code = ? AND m.exam_type = ? AND m.marks IS NOT NULL
        ORDER BY m.marks DESC
        LIMIT ?
    """
    try:
        cursor.execute(sql, (subject_code, exam_type, limit))
        leaderboard_data = cursor.fetchall()
        return [(row[0], row[1]) for row in leaderboard_data]
    except sqlite3.Error as e:
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
                "id": user_data[0],
                "full_name": user_data[1],
                "prn": user_data[2],
                "dob_day": user_data[3],
                "dob_month": user_data[4],
                "dob_year": user_data[5]
            })
        return users_list
    except sqlite3.Error as e:
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
        # SQLite doesn't support ON CONFLICT DO UPDATE directly in older versions
        # So we'll use INSERT OR REPLACE
        cursor.execute("""
            INSERT OR REPLACE INTO semester_records 
            (user_id, semester_number, semester_name, sgpa, total_credits, academic_year, created_at)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """, (user_id, semester_number, semester_name, sgpa, total_credits, academic_year))
        
        conn.commit()
        print(f"Semester {semester_number} record saved/updated for user_id {user_id}.")
        return True
    except sqlite3.Error as e:
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
        WHERE user_id = ?
        ORDER BY semester_number ASC
    '''
    try:
        cursor.execute(sql, (user_id,))
        records = cursor.fetchall()
        semester_list = []
        for record in records:
            semester_list.append({
                "semester_number": record[0],
                "semester_name": record[1],
                "sgpa": float(record[2]) if record[2] else None,
                "total_credits": record[3],
                "academic_year": record[4],
                "created_at": record[5]
            })
        return semester_list
    except sqlite3.Error as e:
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
        WHERE user_id = ?
        ORDER BY subject_code, exam_type
    '''
    try:
        cursor.execute(sql, (user_id,))
        marks_records = cursor.fetchall()
        
        cie_marks_dict = {}
        for subject_code, exam_type, marks in marks_records:
            if subject_code not in cie_marks_dict:
                cie_marks_dict[subject_code] = {}
            cie_marks_dict[subject_code][exam_type] = float(marks) if marks else None
        
        return cie_marks_dict
    except sqlite3.Error as e:
        print(f"Error fetching CIE marks: {e}")
        return {}
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
