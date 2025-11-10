"""
Quick script to add a test user to Prisma database
"""
from dotenv import load_dotenv
load_dotenv()

import db_utils_prisma as db

print("=" * 60)
print("Adding Test User to Prisma Database")
print("=" * 60)

# Create tables if they don't exist
print("\n1. Creating tables...")
db.create_db_and_table_pg()

# Add a test user
print("\n2. Adding test user...")
success = db.add_user_to_db_pg(
    first_name="testuser",
    full_name="Test User",
    prn="2021TEST001",
    dob_day="15",
    dob_month="08",
    dob_year="2003"
)

if success:
    print("✅ User added successfully!")
    
    # Retrieve and display
    print("\n3. Retrieving user...")
    user = db.get_user_from_db_pg("testuser")
    
    if user:
        print(f"\n✅ User Details:")
        print(f"   ID: {user['id']}")
        print(f"   Full Name: {user['full_name']}")
        print(f"   PRN: {user['prn']}")
        print(f"   DOB: {user['dob_day']}/{user['dob_month']}/{user['dob_year']}")
        
        print("\n✅ Now check Prisma Studio - you should see the user!")
        print("   http://localhost:5555")
    else:
        print("❌ Could not retrieve user")
else:
    print("❌ Failed to add user")
    print("   This might mean the user already exists")

print("\n" + "=" * 60)
