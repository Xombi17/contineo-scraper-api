# Project Structure

This document explains the organization of the Contineo Scraper API project.

## 📁 Directory Layout

```
contineo-scraper/
├── api.py                      # FastAPI backend application
├── analytics.py                # Analytics engine (performance, predictions)
├── cgpa_calculator.py          # CGPA/SGPA calculation engine
├── web_scraper.py              # Web scraping logic
├── config.py                   # Configuration and subject mappings
├── exam_max_marks.py           # Exam maximum marks configuration
├── db_utils_neon.py            # Neon PostgreSQL utilities
├── db_utils_prisma.py          # Prisma Postgres utilities
├── migrate_to_prisma.py        # Data migration script
├── requirements.txt            # Python dependencies
├── package.json                # Node.js dependencies (Prisma)
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore rules
├── Dockerfile                  # Docker container config
├── docker-compose.yml          # Docker Compose config
├── vercel.json                 # Vercel deployment config
├── API_DOCUMENTATION.md        # Complete API reference
├── DEPLOYMENT_GUIDE.md         # Deployment instructions
├── PRISMA_SETUP.md             # Prisma setup guide
├── README.md                   # Project overview
├── prisma/                     # Prisma ORM
│   ├── schema.prisma           # Database schema
│   └── migrations/             # Database migrations
├── docs/                       # Documentation
│   ├── MAX_MARKS_UPDATE.md
│   ├── PROJECT_STRUCTURE.md    # This file
│   └── README.md
└── scripts/                    # Utility scripts
    ├── manage_user.py          # User management CLI
    ├── register_user.py        # User registration CLI
    └── update_all.py           # Batch update script
```

## 🎯 Core Application Files

### Backend API
- **api.py**: FastAPI application with all REST endpoints
  - User management
  - Data fetching
  - CGPA/SGPA calculations
  - Analytics endpoints
  - Leaderboards

### Analytics Engine
- **analytics.py**: Advanced analytics features
  - Subject performance dashboard
  - Attendance-marks correlation
  - Semester comparison
  - Grade predictions

### Calculation Engine
- **cgpa_calculator.py**: CGPA/SGPA calculations
  - Grade point conversion
  - SGPA calculation
  - CGPA calculation
  - Target grade calculator

### Data Scraping
- **web_scraper.py**: Portal scraping logic
  - Login automation
  - Attendance extraction
  - CIE marks extraction

### Configuration
- **config.py**: Application configuration
  - Database connection strings
  - Subject code mappings
  - Credit hours configuration
  - Portal URLs

- **exam_max_marks.py**: Exam marks configuration
  - Maximum marks per exam type
  - Subject-specific overrides

### Database Utilities
- **db_utils_neon.py**: Neon PostgreSQL operations
  - User CRUD operations
  - Marks management
  - Semester records
  - Leaderboards

- **db_utils_prisma.py**: Prisma Postgres operations
  - Same interface as Neon utilities
  - Works with Prisma database

- **migrate_to_prisma.py**: Data migration script
  - Migrate from Neon to Prisma
  - Handles all tables
  - Maintains relationships

## 📚 Documentation Files

### Main Documentation
- **README.md**: Project overview and quick start
- **API_DOCUMENTATION.md**: Complete API reference with examples
- **DEPLOYMENT_GUIDE.md**: Deployment instructions for various platforms
- **PRISMA_SETUP.md**: Prisma ORM setup and usage guide

### Docs Folder
- **docs/README.md**: Documentation index
- **docs/PROJECT_STRUCTURE.md**: This file
- **docs/MAX_MARKS_UPDATE.md**: Max marks calculation documentation

## 🐳 Deployment Files

### Docker
- **Dockerfile**: Container image definition
- **docker-compose.yml**: Multi-container setup
- **.dockerignore**: Files to exclude from Docker build

### Cloud Platforms
- **vercel.json**: Vercel deployment configuration

## 🗄️ Database

### Prisma
- **prisma/schema.prisma**: Database schema definition
- **prisma/migrations/**: Database migration history
- **prisma.config.ts**: Prisma configuration

### Tables
- **users**: Student credentials and information
- **cie_marks**: CIE marks for leaderboards
- **semester_records**: Saved semester data for CGPA tracking

## 🛠️ Utility Scripts

### User Management
- **scripts/register_user.py**: CLI for registering new users
- **scripts/manage_user.py**: CLI for managing existing users

### Batch Operations
- **scripts/update_all.py**: Update data for all registered users

## 📦 Dependencies

### Python (requirements.txt)
- fastapi: Web framework
- uvicorn: ASGI server
- psycopg2-binary: PostgreSQL adapter
- beautifulsoup4: HTML parsing
- requests: HTTP client
- python-dotenv: Environment variables
- pytz: Timezone handling

### Node.js (package.json)
- @prisma/client: Prisma ORM client
- prisma: Prisma CLI
- dotenv: Environment variables

## 🔄 Data Flow

1. **User Registration**
   - User submits credentials via API
   - Credentials validated by logging into portal
   - User stored in database

2. **Data Fetching**
   - API receives username
   - Retrieves credentials from database
   - Logs into portal
   - Scrapes attendance and marks
   - Stores in database
   - Returns to client

3. **Analytics**
   - API receives username
   - Retrieves data from database
   - Performs calculations
   - Returns insights

4. **CGPA Calculation**
   - Retrieves marks from database
   - Calculates grade points
   - Computes SGPA/CGPA
   - Saves semester records

## 🎨 Architecture

### Backend (Python)
- FastAPI REST API
- PostgreSQL database (Neon or Prisma)
- Web scraping with BeautifulSoup
- Analytics engine

### Frontend (Next.js - Separate Repo)
- Consumes REST API
- Prisma Client for direct DB access
- React components
- Charts and visualizations

## 🔐 Security

### Environment Variables
- Database credentials
- API keys
- Portal credentials (encrypted)

### Best Practices
- Password hashing (TODO)
- API authentication (TODO)
- Rate limiting (TODO)
- Input validation
- SQL injection prevention (parameterized queries)

## 📊 Analytics Features

### Performance Dashboard
- Subject-wise metrics
- Overall statistics
- Weak/strong subject identification
- Completion tracking

### Correlation Analysis
- Attendance vs marks correlation
- Statistical insights
- Subject-by-subject comparison

### Semester Comparison
- SGPA trends
- Improvement tracking
- Best semester identification

### Grade Predictions
- ESE requirements for target grades
- Achievability analysis
- Recommendations

## 🚀 Deployment Options

1. **Docker**: Containerized deployment
2. **Vercel**: Serverless deployment
3. **Railway**: Platform-as-a-Service
4. **Render**: Web service deployment
5. **AWS EC2**: Virtual machine deployment

## 📝 Notes

- All database operations use parameterized queries
- Timezone-aware timestamps (UTC)
- Graceful error handling
- Comprehensive logging
- API documentation with Swagger UI
- Type hints throughout codebase
