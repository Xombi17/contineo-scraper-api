# Project Structure

This document explains the organization of the Contineo Scraper project.

## Directory Layout

```
contineo-scraper/
├── main.py                  # CLI application
├── st_main.py              # Streamlit web interface
├── web_scraper.py          # Web scraping logic
├── db_utils_neon.py        # Neon PostgreSQL database operations
├── cgpa_calculator.py      # CGPA/SGPA calculation engine
├── config.py               # Configuration and subject mappings
├── exam_max_marks.py       # Exam maximum marks configuration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repository)
├── README.md               # Project overview
├── FINAL_ORGANIZATION_SUMMARY.md  # Summary of organization work
├── docs/                   # Documentation files
│   ├── CLEANUP_SUMMARY.md
│   ├── MAX_MARKS_UPDATE.md
│   ├── PROJECT_STRUCTURE.md (this file)
│   ├── QUICK_REFERENCE.md
│   ├── README.md
│   └── SQLITE_MIGRATION_COMPLETE.md
├── scripts/                # Utility scripts
│   ├── debug_calculation.py
│   ├── init_sqlite_db.py
│   ├── manage_user.py
│   ├── register_user.py
│   └── update_all.py
└── utils/                  # Utility functions (currently empty)
```

## Core Application Files

### Main Application Files
- **[main.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/main.py)**: Command-line interface for the application
- **[st_main.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/st_main.py)**: Streamlit web interface with CGPA calculator
- **[web_scraper.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/web_scraper.py)**: Logic for scraping data from the Contineo portal
- **[db_utils_neon.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/db_utils_neon.py)**: Database operations using Neon PostgreSQL
- **[cgpa_calculator.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/cgpa_calculator.py)**: CGPA/SGPA calculation engine
- **[config.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/config.py)**: Configuration settings and subject mappings
- **[exam_max_marks.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/exam_max_marks.py)**: Exam maximum marks configuration

### Database
- **Neon PostgreSQL**: Cloud database hosted on Neon.tech
- Tables: users, cie_marks, semester_records

### Configuration
- **[requirements.txt](file:///c:/Users/varad/Documents/Github/contineo-scraper/requirements.txt)**: Python dependencies
- **[.env](file:///c:/Users/varad/Documents/Github/contineo-scraper/.env)**: Environment variables (not in repository for security)

## Documentation Files

### User Guides
- **[QUICK_REFERENCE.md](file:///c:/Users/varad/Documents/Github/contineo-scraper/docs/QUICK_REFERENCE.md)**: Quick reference cheat sheet for common operations
- **[MAX_MARKS_UPDATE.md](file:///c:/Users/varad/Documents/Github/contineo-scraper/docs/MAX_MARKS_UPDATE.md)**: Documentation on the max marks calculation update
- **[SQLITE_MIGRATION_COMPLETE.md](file:///c:/Users/varad/Documents/Github/contineo-scraper/docs/SQLITE_MIGRATION_COMPLETE.md)**: Documentation on the migration from SQLite to Neon PostgreSQL

### Technical Documentation
- **[README.md](file:///c:/Users/varad/Documents/Github/contineo-scraper/docs/README.md)**: Project overview and getting started guide
- **[PROJECT_STRUCTURE.md](file:///c:/Users/varad/Documents/Github/contineo-scraper/docs/PROJECT_STRUCTURE.md)**: This file
- **[CLEANUP_SUMMARY.md](file:///c:/Users/varad/Documents/Github/contineo-scraper/docs/CLEANUP_SUMMARY.md)**: Summary of cleanup work performed

## Scripts Directory

The **scripts/** directory contains utility scripts for various operations:

### User Management
- **[register_user.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/scripts/register_user.py)**: Register a new user
- **[manage_user.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/scripts/manage_user.py)**: Comprehensive user management tool

### Database Operations
- **[init_sqlite_db.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/scripts/init_sqlite_db.py)**: Initialize the Neon PostgreSQL database
- **[debug_calculation.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/scripts/debug_calculation.py)**: Debug CGPA calculations

### Batch Operations
- **[update_all.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/scripts/update_all.py)**: Update data for all registered users

## Utils Directory

The **utils/** directory is reserved for utility functions that may be added in the future.

## Best Practices

1. **Modularity**: Each file has a specific purpose and responsibility
2. **Configuration**: All configuration is centralized in [config.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/config.py)
3. **Database**: All database operations are handled by [db_utils_neon.py](file:///c:/Users/varad/Documents/Github/contineo-scraper/db_utils_neon.py)
4. **Documentation**: Comprehensive documentation is maintained in the **docs/** directory
5. **Scripts**: Utility scripts are organized in the **scripts/** directory for easy access