#!/usr/bin/env python3
"""
User Management Script
Can create a new user or update an existing user's username and PRN
"""

import psycopg2  # Changed from sqlite3 to psycopg2
import db_utils_neon as db_utils  # Changed from db_utils_sqlite to db_utils_neon

def update_user_username_and_prn(old_username, new_username, new_prn):
    """
    Update an existing user's username and PRN
    
    Args:
        old_username (str): The current username of the user
        new_username (str): The new username to set
        new_prn (str): The new PRN to set
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get user data using the db_utils function
        user_data = db_utils.get_user_from_db_pg(old_username)
        
        if not user_data:
            print(f"User with username '{old_username}' not found")
            return False
            
        user_id = user_data["id"]
        full_name = user_data["full_name"]
        current_prn = user_data["prn"]
        dob_day = user_data["dob_day"]
        dob_month = user_data["dob_month"]
        dob_year = user_data["dob_year"]
        
        print(f"Found user: {full_name} (ID: {user_id})")
        print(f"Current username: {old_username}")
        print(f"Current PRN: {current_prn}")
        print(f"New username: {new_username}")
        print(f"New PRN: {new_prn}")
        
        # Get database connection
        conn = db_utils.get_db_connection()
        if not conn:
            print("Failed to connect to database")
            return False
            
        cursor = conn.cursor()
        
        # Update the username and PRN
        cursor.execute("UPDATE users SET first_name = %s, prn = %s WHERE id = %s", (new_username.lower().strip(), new_prn, user_id))
        conn.commit()
        
        # Verify the update by fetching the user again
        updated_user_data = db_utils.get_user_from_db_pg(new_username)
        
        if updated_user_data and updated_user_data["id"] == user_id and updated_user_data["prn"] == new_prn:
            print(f"✅ Successfully updated user")
            print(f"   Username: {old_username} → {new_username}")
            print(f"   PRN: {current_prn} → {new_prn}")
            return True
        else:
            print("❌ Failed to update user")
            return False
            
    except psycopg2.Error as e:  # Changed from sqlite3.Error to psycopg2.Error
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    finally:
        # Connection will be closed by db_utils functions


def create_user(username, full_name, prn, dob_day, dob_month, dob_year):
    """
    Create a new user with the specified details
    
    Args:
        username (str): The username for the new user
        full_name (str): The full name of the user
        prn (str): The PRN of the user
        dob_day (str): Day of birth
        dob_month (str): Month of birth
        dob_year (str): Year of birth
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Use the existing function from db_utils
        result = db_utils.add_user_to_db_pg(username, full_name, prn, dob_day, dob_month, dob_year)
        if result:
            print(f"✅ Successfully created user '{username}' with PRN '{prn}'")
        else:
            print(f"❌ Failed to create user '{username}'")
        return result
    except Exception as e:
        print(f"Error creating user: {e}")
        return False


def list_all_users():
    """List all users in the database"""
    try:
        all_users = db_utils.get_all_users_from_db_pg()
        
        if all_users:
            print("\nExisting users in database:")
            print("-" * 60)
            for user_data in all_users:
                print(f"  ID: {user_data['id']:2d} | Username: '{user_data['first_name']:10s}' | Full Name: {user_data['full_name']:20s} | PRN: {user_data['prn']}")
        else:
            print("\nNo users found in database")
            
    except Exception as e:
        print(f"Error listing users: {e}")


if __name__ == "__main__":
    print("User Management Tool")
    print("=" * 50)
    
    # List current users
    list_all_users()
    
    print("\n" + "=" * 50)
    print("Options:")
    print("1. Update existing user's username and PRN")
    print("2. Create new user")
    
    try:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        
        if choice == "1":
            print("\nUpdate existing user")
            old_username = input("Enter current username (e.g., 'xombi7'): ").strip()
            new_username = input("Enter new username (e.g., 'Xombi17'): ").strip()
            new_prn = input("Enter new PRN (e.g., 'MU0341120240233090'): ").strip()
            
            if all([old_username, new_username, new_prn]):
                success = update_user_username_and_prn(old_username, new_username, new_prn)
                if success:
                    print("\n🎉 User update completed successfully!")
                else:
                    print("\n❌ User update failed!")
            else:
                print("\n❌ All fields are required!")
                
        elif choice == "2":
            print("\nCreate new user")
            username = input("Enter username (e.g., 'Xombi17'): ").strip()
            full_name = input("Enter full name: ").strip()
            prn = input("Enter PRN (e.g., 'MU0341120240233090'): ").strip()
            dob_day = input("Enter day of birth (e.g., '01'): ").strip()
            dob_month = input("Enter month of birth (e.g., '01'): ").strip()
            dob_year = input("Enter year of birth (e.g., '2000'): ").strip()
            
            if all([username, full_name, prn, dob_day, dob_month, dob_year]):
                success = create_user(username, full_name, prn, dob_day, dob_month, dob_year)
                if success:
                    print("\n🎉 User creation completed successfully!")
                else:
                    print("\n❌ User creation failed!")
            else:
                print("\n❌ All fields are required!")
        else:
            print("\n❌ Invalid choice!")
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")