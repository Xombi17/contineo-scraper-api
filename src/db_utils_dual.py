"""
Dual Database Utilities
Writes to both Neon and Prisma databases simultaneously
"""

import db_utils_neon
import db_utils_prisma
from typing import Dict, List, Optional
from datetime import datetime

DB_NAME_FOR_MESSAGES = "Dual Database (Neon + Prisma)"

def create_db_and_table_pg():
    """Creates tables in both databases"""
    print("Creating tables in both Neon and Prisma...")
    db_utils_neon.create_db_and_table_pg()
    db_utils_prisma.create_db_and_table_pg()
    print("✅ Tables created in both databases")

def add_user_to_db_pg(first_name, full_name, prn, dob_day, dob_month, dob_year):
    """Adds user to both Neon and Prisma databases"""
    print(f"Adding user '{full_name}' to both databases...")
    
    # Add to Neon
    neon_success = db_utils_neon.add_user_to_db_pg(
        first_name, full_name, prn, dob_day, dob_month, dob_year
    )
    
    # Add to Prisma
    prisma_success = db_utils_prisma.add_user_to_db_pg(
        first_name, full_name, prn, dob_day, dob_month, dob_year
    )
    
    if neon_success and prisma_success:
        print(f"✅ User '{full_name}' added to BOTH databases")
        return True
    elif neon_success:
        print(f"⚠️ User added to Neon only (Prisma failed)")
        return True
    elif prisma_success:
        print(f"⚠️ User added to Prisma only (Neon failed)")
        return True
    else:
        print(f"❌ Failed to add user to both databases")
        return False

def get_user_from_db_pg(first_name_query):
    """Retrieves user from Neon (primary database)"""
    # Try Neon first
    user = db_utils_neon.get_user_from_db_pg(first_name_query)
    if user:
        return user
    
    # Fallback to Prisma
    return db_utils_prisma.get_user_from_db_pg(first_name_query)

def update_student_marks_in_db_pg(user_id, cie_marks_data, scraped_timestamp):
    """Updates marks in both databases"""
    # Update in Neon
    neon_success = db_utils_neon.update_student_marks_in_db_pg(
        user_id, cie_marks_data, scraped_timestamp
    )
    
    # Update in Prisma
    prisma_success = db_utils_prisma.update_student_marks_in_db_pg(
        user_id, cie_marks_data, scraped_timestamp
    )
    
    return neon_success or prisma_success

def get_subject_leaderboard_pg(subject_code, exam_type, limit=3):
    """Gets leaderboard from Neon (primary database)"""
    return db_utils_neon.get_subject_leaderboard_pg(subject_code, exam_type, limit)

def get_all_users_from_db_pg():
    """Gets all users from Neon (primary database)"""
    return db_utils_neon.get_all_users_from_db_pg()

def save_semester_record_pg(user_id, semester_number, semester_name, sgpa, total_credits, academic_year=None):
    """Saves semester record to both databases"""
    # Save to Neon
    neon_success = db_utils_neon.save_semester_record_pg(
        user_id, semester_number, semester_name, sgpa, total_credits, academic_year
    )
    
    # Save to Prisma
    prisma_success = db_utils_prisma.save_semester_record_pg(
        user_id, semester_number, semester_name, sgpa, total_credits, academic_year
    )
    
    return neon_success or prisma_success

def get_user_semester_records_pg(user_id):
    """Gets semester records from Neon (primary database)"""
    return db_utils_neon.get_user_semester_records_pg(user_id)

def get_user_current_cie_marks_pg(user_id):
    """Gets CIE marks from Neon (primary database)"""
    return db_utils_neon.get_user_current_cie_marks_pg(user_id)
