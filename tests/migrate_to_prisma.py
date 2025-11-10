"""
Data Migration Script: Neon PostgreSQL → Prisma Postgres
Migrates all users, CIE marks, and semester records
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# Source: Neon PostgreSQL
NEON_PASSWORD = os.getenv("NEON_DB_PASSWORD")
NEON_URI = os.getenv("NEON_DB_URI")
NEON_DBNAME = os.getenv("PG_DBNAME")
NEON_USER = os.getenv("PG_USER")

NEON_CONN_STRING = f"postgresql://{NEON_USER}:{NEON_PASSWORD}@{NEON_URI}/{NEON_DBNAME}?sslmode=require"

# Target: Prisma Postgres
PRISMA_DIRECT_URL = os.getenv("DIRECT_URL")

def get_neon_connection():
    """Connect to Neon PostgreSQL"""
    try:
        conn = psycopg2.connect(NEON_CONN_STRING, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to Neon: {e}")
        return None

def get_prisma_connection():
    """Connect to Prisma Postgres"""
    try:
        conn = psycopg2.connect(PRISMA_DIRECT_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to Prisma Postgres: {e}")
        return None

def migrate_users(source_conn, target_conn):
    """Migrate users table"""
    print("\n📊 Migrating Users...")
    
    source_cursor = source_conn.cursor()
    target_cursor = target_conn.cursor()
    
    # Fetch all users from Neon
    source_cursor.execute("SELECT * FROM users ORDER BY id")
    users = source_cursor.fetchall()
    
    if not users:
        print("  ⚠️  No users found in source database")
        return {}
    
    print(f"  Found {len(users)} users to migrate")
    
    # User ID mapping (old_id -> new_id)
    id_mapping = {}
    
    for user in users:
        try:
            # Insert into Prisma Postgres
            target_cursor.execute("""
                INSERT INTO users (first_name, full_name, prn, dob_day, dob_month, dob_year)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (first_name) DO UPDATE SET
                    full_name = EXCLUDED.full_name,
                    prn = EXCLUDED.prn,
                    dob_day = EXCLUDED.dob_day,
                    dob_month = EXCLUDED.dob_month,
                    dob_year = EXCLUDED.dob_year
                RETURNING id
            """, (
                user['first_name'],
                user['full_name'],
                user['prn'],
                user['dob_day'],
                user['dob_month'],
                user['dob_year']
            ))
            
            new_id = target_cursor.fetchone()['id']
            id_mapping[user['id']] = new_id
            
            print(f"  ✅ Migrated user: {user['full_name']} (ID: {user['id']} → {new_id})")
            
        except Exception as e:
            print(f"  ❌ Failed to migrate user {user['full_name']}: {e}")
    
    target_conn.commit()
    print(f"\n✅ Users migration complete! Migrated {len(id_mapping)} users")
    
    return id_mapping

def migrate_cie_marks(source_conn, target_conn, id_mapping):
    """Migrate CIE marks table"""
    print("\n📊 Migrating CIE Marks...")
    
    source_cursor = source_conn.cursor()
    target_cursor = target_conn.cursor()
    
    # Fetch all CIE marks from Neon
    source_cursor.execute("SELECT * FROM cie_marks ORDER BY user_id, subject_code, exam_type")
    marks = source_cursor.fetchall()
    
    if not marks:
        print("  ⚠️  No CIE marks found in source database")
        return
    
    print(f"  Found {len(marks)} CIE mark records to migrate")
    
    migrated_count = 0
    skipped_count = 0
    
    for mark in marks:
        old_user_id = mark['user_id']
        
        # Skip if user wasn't migrated
        if old_user_id not in id_mapping:
            skipped_count += 1
            continue
        
        new_user_id = id_mapping[old_user_id]
        
        try:
            target_cursor.execute("""
                INSERT INTO cie_marks (user_id, subject_code, exam_type, marks, scraped_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id, subject_code, exam_type) DO UPDATE SET
                    marks = EXCLUDED.marks,
                    scraped_at = EXCLUDED.scraped_at
            """, (
                new_user_id,
                mark['subject_code'],
                mark['exam_type'],
                mark['marks'],
                mark['scraped_at']
            ))
            
            migrated_count += 1
            
        except Exception as e:
            print(f"  ❌ Failed to migrate mark for user {old_user_id}: {e}")
            skipped_count += 1
    
    target_conn.commit()
    print(f"\n✅ CIE Marks migration complete!")
    print(f"  Migrated: {migrated_count}")
    print(f"  Skipped: {skipped_count}")

def migrate_semester_records(source_conn, target_conn, id_mapping):
    """Migrate semester records table"""
    print("\n📊 Migrating Semester Records...")
    
    source_cursor = source_conn.cursor()
    target_cursor = target_conn.cursor()
    
    # Fetch all semester records from Neon
    source_cursor.execute("SELECT * FROM semester_records ORDER BY user_id, semester_number")
    records = source_cursor.fetchall()
    
    if not records:
        print("  ⚠️  No semester records found in source database")
        return
    
    print(f"  Found {len(records)} semester records to migrate")
    
    migrated_count = 0
    skipped_count = 0
    
    for record in records:
        old_user_id = record['user_id']
        
        # Skip if user wasn't migrated
        if old_user_id not in id_mapping:
            skipped_count += 1
            continue
        
        new_user_id = id_mapping[old_user_id]
        
        try:
            target_cursor.execute("""
                INSERT INTO semester_records 
                (user_id, semester_number, semester_name, sgpa, total_credits, academic_year, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id, semester_number) DO UPDATE SET
                    semester_name = EXCLUDED.semester_name,
                    sgpa = EXCLUDED.sgpa,
                    total_credits = EXCLUDED.total_credits,
                    academic_year = EXCLUDED.academic_year,
                    created_at = EXCLUDED.created_at
            """, (
                new_user_id,
                record['semester_number'],
                record['semester_name'],
                record['sgpa'],
                record['total_credits'],
                record['academic_year'],
                record['created_at']
            ))
            
            migrated_count += 1
            
        except Exception as e:
            print(f"  ❌ Failed to migrate semester record for user {old_user_id}: {e}")
            skipped_count += 1
    
    target_conn.commit()
    print(f"\n✅ Semester Records migration complete!")
    print(f"  Migrated: {migrated_count}")
    print(f"  Skipped: {skipped_count}")

def verify_migration(target_conn):
    """Verify the migration was successful"""
    print("\n🔍 Verifying Migration...")
    
    cursor = target_conn.cursor()
    
    # Count records
    cursor.execute("SELECT COUNT(*) as count FROM users")
    user_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM cie_marks")
    marks_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM semester_records")
    semester_count = cursor.fetchone()['count']
    
    print(f"\n📊 Migration Summary:")
    print(f"  Users: {user_count}")
    print(f"  CIE Marks: {marks_count}")
    print(f"  Semester Records: {semester_count}")
    
    # Sample data
    cursor.execute("SELECT first_name, full_name FROM users LIMIT 3")
    sample_users = cursor.fetchall()
    
    if sample_users:
        print(f"\n👥 Sample Users:")
        for user in sample_users:
            print(f"  • {user['full_name']} ({user['first_name']})")

def main():
    print("=" * 60)
    print("🚀 Data Migration: Neon → Prisma Postgres")
    print("=" * 60)
    
    # Connect to both databases
    print("\n🔌 Connecting to databases...")
    
    source_conn = get_neon_connection()
    if not source_conn:
        print("❌ Cannot proceed without source connection")
        return
    print("  ✅ Connected to Neon PostgreSQL")
    
    target_conn = get_prisma_connection()
    if not target_conn:
        print("❌ Cannot proceed without target connection")
        source_conn.close()
        return
    print("  ✅ Connected to Prisma Postgres")
    
    try:
        # Migrate data
        id_mapping = migrate_users(source_conn, target_conn)
        
        if id_mapping:
            migrate_cie_marks(source_conn, target_conn, id_mapping)
            migrate_semester_records(source_conn, target_conn, id_mapping)
        
        # Verify
        verify_migration(target_conn)
        
        print("\n" + "=" * 60)
        print("✅ Migration Complete!")
        print("=" * 60)
        print("\nYour data is now available in Prisma Postgres!")
        print("Remember to claim your database to keep it beyond 24 hours:")
        print("https://create-db.prisma.io/claim?projectID=proj_cmhtj549u04mezzf251o38c3l")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Close connections
        if source_conn:
            source_conn.close()
        if target_conn:
            target_conn.close()
        print("\n🔌 Database connections closed")

if __name__ == "__main__":
    main()
