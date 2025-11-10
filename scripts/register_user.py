#!/usr/bin/env python3
"""
Quick Registration Helper
Helps you register your Contineo account in the database
"""

import db_utils_neon as db_utils  # Changed from db_utils_sqlite to db_utils_neon
import web_scraper

def register_user():
    print("=" * 60)
    print("  CONTINEO SCRAPER - USER REGISTRATION")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing database...")
    db_utils.create_db_and_table_pg()
    print("   ✓ Database ready!")
    
    # Get user input
    print("\n2. Enter your details:")
    print("   (These must match your Contineo portal login)")
    print()
    
    username = input("   Username (e.g., 'xombi17'): ").strip()
    full_name = input("   Full Name (exact match): ").strip()
    prn = input("   PRN/Roll No: ").strip()
    dob_day = input("   DOB Day (e.g., 15): ").strip()
    dob_month = input("   DOB Month (e.g., 08): ").strip()
    dob_year = input("   DOB Year (e.g., 2004): ").strip()
    
    # Validate fields
    if not all([username, full_name, prn, dob_day, dob_month, dob_year]):
        print("\n   ✗ Error: All fields are required!")
        return False
    
    # Test login
    print("\n3. Validating credentials with Contineo portal...")
    try:
        _, html = web_scraper.login_and_get_welcome_page(
            prn, dob_day, dob_month, dob_year, full_name
        )
        
        if not html:
            print("   ✗ Login failed! Please check your credentials.")
            print("   Make sure Full Name, PRN, and DOB match the portal exactly.")
            return False
        
        print("   ✓ Credentials validated successfully!")
        
    except Exception as e:
        print(f"   ✗ Error during validation: {e}")
        return False
    
    # Save to database
    print("\n4. Saving to database...")
    if db_utils.add_user_to_db_pg(username, full_name, prn, dob_day, dob_month, dob_year):
        print("   ✓ User registered successfully!")
        print("\n" + "=" * 60)
        print(f"  SUCCESS! You can now use username '{username}'")
        print("  in the Streamlit app to fetch your data.")
        print("=" * 60)
        return True
    else:
        print("   ✗ Failed to save. Username or PRN might already exist.")
        return False

if __name__ == "__main__":
    try:
        register_user()
    except KeyboardInterrupt:
        print("\n\nRegistration cancelled.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")