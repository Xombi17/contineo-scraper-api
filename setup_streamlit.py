#!/usr/bin/env python3
"""
Setup script for Streamlit deployment
Helps configure database connections and verify setup
"""

import os
import sys

def check_requirements():
    """Check if all required packages are installed"""
    required = [
        'streamlit',
        'psycopg2',
        'plotly',
        'beautifulsoup4',
        'requests',
        'python-dotenv'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nInstall with: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages installed")
    return True

def check_database_config():
    """Check if database configuration is present"""
    has_env = os.path.exists('.env')
    has_secrets = os.path.exists('.streamlit/secrets.toml')
    
    if not has_env and not has_secrets:
        print("⚠️  No database configuration found!")
        print("\nFor local development, create .env file with:")
        print("   DIRECT_URL=postgresql://user:pass@host:port/db")
        print("\nFor Streamlit Cloud, add secrets in the dashboard")
        return False
    
    if has_env:
        print("✅ Found .env file for local development")
    
    if has_secrets:
        print("✅ Found .streamlit/secrets.toml")
    
    return True

def test_database_connection():
    """Test database connection"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Try importing streamlit to use secrets if available
        try:
            import streamlit as st
            db_url = st.secrets.get("DIRECT_URL") or os.getenv("DIRECT_URL")
        except:
            db_url = os.getenv("DIRECT_URL")
        
        if not db_url:
            print("⚠️  DIRECT_URL not configured")
            return False
        
        import psycopg2
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        
        print("✅ Database connection successful!")
        print(f"   PostgreSQL version: {version[0].split(',')[0]}")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_streamlit_config():
    """Create .streamlit directory and config if not exists"""
    os.makedirs('.streamlit', exist_ok=True)
    
    config_path = '.streamlit/config.toml'
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            f.write("""[theme]
primaryColor = "#6366f1"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f3f4f6"
textColor = "#1f2937"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
""")
        print("✅ Created .streamlit/config.toml")
    else:
        print("✅ .streamlit/config.toml already exists")

def main():
    print("🎓 Streamlit Deployment Setup\n")
    print("=" * 50)
    
    # Check requirements
    print("\n1. Checking Python packages...")
    if not check_requirements():
        sys.exit(1)
    
    # Create Streamlit config
    print("\n2. Setting up Streamlit configuration...")
    create_streamlit_config()
    
    # Check database config
    print("\n3. Checking database configuration...")
    check_database_config()
    
    # Test database connection
    print("\n4. Testing database connection...")
    test_database_connection()
    
    print("\n" + "=" * 50)
    print("\n✨ Setup complete!")
    print("\nNext steps:")
    print("1. Configure database URL in .env or .streamlit/secrets.toml")
    print("2. Run locally: streamlit run src/st_main.py")
    print("3. Deploy to Streamlit Cloud and add secrets there")
    print("\nSee STREAMLIT_DEPLOYMENT.md for detailed instructions")

if __name__ == "__main__":
    main()
