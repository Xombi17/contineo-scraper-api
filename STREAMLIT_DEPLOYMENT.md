# Streamlit Cloud Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Prepare Your Repository

Make sure these files are in your repository:
- `src/st_main.py` - Main Streamlit app
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration (optional)

### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set the main file path: `src/st_main.py`
6. Click "Deploy"

### 3. Configure Secrets

After deployment, you need to add your database credentials:

1. Go to your app's dashboard on Streamlit Cloud
2. Click on "Settings" (⚙️)
3. Click on "Secrets"
4. Add your secrets in TOML format:

```toml
# Database Configuration
DIRECT_URL = "postgresql://user:password@host:port/database?sslmode=require"

# Optional: If using dual database setup
DATABASE_URL = "your_neon_database_url_here"

# Example Prisma Postgres URL:
# DIRECT_URL = "postgresql://neondb_owner:xxxxx@ep-xxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
```

### 4. Get Your Database URLs

#### For Prisma Postgres:
1. Go to your Prisma Data Platform dashboard
2. Navigate to your project
3. Go to "Settings" → "Connection strings"
4. Copy the **Direct URL** (not the pooled URL)
5. Paste it as `DIRECT_URL` in Streamlit secrets

#### For Neon:
1. Go to your Neon console
2. Select your project
3. Go to "Connection Details"
4. Copy the connection string
5. Paste it as `DATABASE_URL` in Streamlit secrets

### 5. Verify Deployment

1. Wait for the app to redeploy (happens automatically after adding secrets)
2. Test the app by:
   - Entering a username
   - Clicking "Fetch Data"
   - Verifying data loads correctly

## 🔧 Troubleshooting

### Database Connection Issues

If you see "Error connecting to database":

1. **Check your connection string format:**
   ```
   postgresql://username:password@host:port/database?sslmode=require
   ```

2. **Verify SSL mode:**
   - Most cloud databases require `?sslmode=require` at the end

3. **Test locally first:**
   ```bash
   # Add to .env file
   DIRECT_URL="your_database_url"
   
   # Run locally
   streamlit run src/st_main.py
   ```

### Missing Dependencies

If you get import errors:

1. Make sure `requirements.txt` includes all dependencies:
   ```
   streamlit
   streamlit-local-storage
   plotly
   psycopg2-binary
   python-dotenv
   beautifulsoup4
   requests
   pytz
   ```

2. Redeploy the app

### Secrets Not Loading

If secrets aren't being read:

1. Make sure the TOML format is correct (no quotes around keys)
2. Restart the app from Streamlit Cloud dashboard
3. Check the app logs for specific errors

## 📝 Local Development

To test locally with the same secrets:

1. Create `.streamlit/secrets.toml` in your project root:
   ```toml
   DIRECT_URL = "your_database_url"
   ```

2. Add `.streamlit/secrets.toml` to `.gitignore`:
   ```
   .streamlit/secrets.toml
   ```

3. Run locally:
   ```bash
   streamlit run src/st_main.py
   ```

## 🔒 Security Best Practices

1. **Never commit secrets to Git:**
   - Add `.streamlit/secrets.toml` to `.gitignore`
   - Use `.env` for local development only

2. **Use environment-specific URLs:**
   - Development: Local database or test database
   - Production: Production database on Streamlit Cloud

3. **Rotate credentials regularly:**
   - Update database passwords periodically
   - Update secrets in Streamlit Cloud when changed

## 📊 Database Setup

Your database should have these tables:

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    prn TEXT NOT NULL UNIQUE,
    dob_day TEXT NOT NULL,
    dob_month TEXT NOT NULL,
    dob_year TEXT NOT NULL
);

-- CIE Marks table
CREATE TABLE cie_marks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    subject_code TEXT NOT NULL,
    exam_type TEXT NOT NULL,
    marks REAL,
    scraped_at TIMESTAMP WITH TIME ZONE NOT NULL,
    UNIQUE (user_id, subject_code, exam_type),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Semester Records table
CREATE TABLE semester_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    semester_number INTEGER NOT NULL,
    semester_name TEXT NOT NULL,
    sgpa REAL,
    total_credits INTEGER,
    academic_year TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, semester_number),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

The app will automatically create these tables on first run if they don't exist.

## 🎨 Customization

### Change Theme Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#6366f1"  # Change to your color
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f3f4f6"
textColor = "#1f2937"
```

### Modify App Settings

Edit `.streamlit/config.toml`:

```toml
[server]
headless = true
port = 8501
maxUploadSize = 200
```

## 📞 Support

If you encounter issues:

1. Check Streamlit Cloud logs
2. Verify database connection strings
3. Test locally first
4. Check that all required secrets are set

## 🔄 Updates

To update your deployed app:

1. Push changes to your GitHub repository
2. Streamlit Cloud will automatically redeploy
3. Monitor the deployment logs for any errors

---

**Note:** The app uses dual database support (Neon + Prisma). If you only have one database, the app will work fine with just `DIRECT_URL` configured.
