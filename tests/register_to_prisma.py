"""
Register a real user to Prisma database with credential validation
"""
from dotenv import load_dotenv
load_dotenv()

import db_utils_prisma as db
import web_scraper

print("=" * 60)
print("Register User to Prisma Database")
print("=" * 60)

# Get user input
print("\nEnter your details:")
username = input("Username (for login): ").strip()
full_name = input("Full Name (as on portal): ").strip()
prn = input("PRN: ").strip()
dob_day = input("DOB Day (01-31): ").strip()
dob_month = input("DOB Month (01-12): ").strip()
dob_year = input("DOB Year: ").strip()

# Validate credentials
print("\n🔍 Validating credentials with Contineo portal...")
session, html = web_scraper.login_and_get_welcome_page(
    prn, dob_day, dob_month, dob_year, full_name
)

if html:
    print("✅ Credentials validated successfully!")
    
    # Add to database
    print("\n💾 Saving to Prisma database...")
    success = db.add_user_to_db_pg(
        username, full_name, prn, dob_day, dob_month, dob_year
    )
    
    if success:
        print(f"\n✅ User '{full_name}' registered successfully!")
        print(f"   Username: {username}")
        print(f"   PRN: {prn}")
        print("\n🎉 You can now use this username to fetch data!")
        print("   Check Prisma Studio: http://localhost:5555")
    else:
        print("\n❌ Failed to save user (username or PRN might already exist)")
else:
    print("\n❌ Credential validation failed!")
    print("   Please check your Full Name, PRN, and DOB")

print("\n" + "=" * 60)
