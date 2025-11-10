# Neon DB Migration

This document explains the migration from SQLite to Neon PostgreSQL database for the Contineo Scraper project.

## Overview

The Contineo Scraper project has been migrated from using a local SQLite database to using Neon PostgreSQL, a serverless Postgres platform. This change provides several benefits:

1. **Cloud Storage**: Data is now stored in the cloud rather than locally
2. **Scalability**: Neon PostgreSQL can handle more concurrent users and larger datasets
3. **Reliability**: Cloud-based database with automatic backups and high availability
4. **Collaboration**: Multiple instances of the application can access the same database

## Changes Made

### 1. Database Utility Files
- **Removed**: `db_utils_sqlite.py`
- **Added**: `db_utils_neon.py` - New database utilities for Neon PostgreSQL

### 2. Configuration Changes
- **Updated**: `config.py` - Now uses Neon PostgreSQL connection parameters
- **Updated**: `.env` - Now requires Neon PostgreSQL credentials

### 3. Application Code Updates
- All application files (`main.py`, `st_main.py`) now import `db_utils_neon` instead of `db_utils_sqlite`
- All script files in the `scripts/` directory updated to use Neon PostgreSQL
- Test files updated to use Neon PostgreSQL

### 4. Dependency Updates
- **Added**: `psycopg2-binary` - PostgreSQL adapter for Python
- **Removed**: SQLite dependencies (no longer needed)

## Database Schema

The database schema remains largely the same, with minor adjustments for PostgreSQL compatibility:

### Users Table
```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    prn TEXT NOT NULL UNIQUE,
    dob_day TEXT NOT NULL,
    dob_month TEXT NOT NULL,
    dob_year TEXT NOT NULL
)
```

### CIE Marks Table
```sql
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
```

### Semester Records Table
```sql
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
```

## Configuration

### Environment Variables
The application now requires the following environment variables in the `.env` file:

```env
NEON_DB_PASSWORD=your_neon_db_password
NEON_DB_URI=your_neon_db_uri  # e.g., ep-spring-voice-a1yre8if-pooler.ap-southeast-1.aws.neon.tech
PG_DBNAME=your_database_name  # e.g., neondb
PG_USER=your_database_user    # e.g., neondb_owner
```

### Connection String
The connection string is constructed as:
```
postgresql://{PG_USER}:{NEON_DB_PASSWORD}@{NEON_DB_URI}/{PG_DBNAME}?sslmode=require
```

## MCP Server Configuration

The project is now configured to work with Neon's MCP (Model Control Protocol) server:

```json
{
  "mcpServers": {
    "Neon": {
      "url": "https://mcp.neon.tech/mcp",
      "headers": {}
    }
  }
}
```

## Benefits of the Migration

### 1. Improved Performance
- PostgreSQL is generally faster for complex queries
- Better indexing and query optimization capabilities

### 2. Enhanced Security
- Professional database security features
- Encrypted connections with SSL/TLS
- Authentication and authorization controls

### 3. Better Data Integrity
- ACID compliance
- Foreign key constraints
- Transaction support

### 4. Scalability
- Automatic scaling based on demand
- Support for concurrent users
- High availability and fault tolerance

## Migration Process

### 1. Data Migration
If you have existing data in SQLite that needs to be migrated:
1. Export data from SQLite database
2. Transform data to match PostgreSQL schema
3. Import data into Neon PostgreSQL database

### 2. Code Updates
All references to `db_utils_sqlite` were replaced with `db_utils_neon`:
- Import statements updated
- Function calls remain the same (same API)
- Database-specific SQL syntax updated for PostgreSQL

### 3. Testing
- All existing tests were updated to use Neon PostgreSQL
- New tests were added to verify PostgreSQL-specific functionality
- Integration tests were run to ensure application works with new database

## Rollback Plan

If you need to rollback to SQLite:
1. Restore the `db_utils_sqlite.py` file
2. Update import statements to use `db_utils_sqlite`
3. Update `config.py` to use SQLite configuration
4. Restore SQLite database file if available

## Future Enhancements

With the migration to Neon PostgreSQL, we can now consider:
- Advanced analytics and reporting
- Real-time data synchronization
- Integration with other cloud services
- Enhanced backup and recovery options