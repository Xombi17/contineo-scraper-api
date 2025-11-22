# Project Structure

## 📁 Organized Directory Layout

```
contineo-scraper/
├── src/                        # Core application code
│   ├── __init__.py            # Package initialization
│   ├── api.py                 # FastAPI backend
│   ├── st_main.py             # Streamlit web app
│   ├── analytics.py           # Analytics engine
│   ├── cgpa_calculator.py     # CGPA/SGPA calculator
│   ├── web_scraper.py         # Portal scraper
│   ├── config.py              # Configuration
│   ├── exam_max_marks.py      # Exam marks config
│   ├── db_utils_neon.py       # Neon database utilities
│   └── db_utils_prisma.py     # Prisma database utilities
│
├── tests/                      # Test and utility scripts
│   ├── test_add_user.py       # Test user creation
│   ├── register_to_prisma.py  # Register user script
│   └── migrate_to_prisma.py   # Data migration script
│
├── scripts/                    # Utility scripts
│   ├── manage_user.py         # User management CLI
│   ├── register_user.py       # User registration CLI
│   └── update_all.py          # Batch update script
│
├── deployment/                 # Deployment configurations
│   ├── Dockerfile             # Docker container
│   ├── docker-compose.yml     # Docker Compose
│   ├── .dockerignore          # Docker ignore rules
│   └── vercel.json            # Vercel deployment
│
├── prisma/                     # Prisma ORM
│   ├── schema.prisma          # Database schema
│   └── migrations/            # Database migrations
│
├── docs/                       # Documentation
│   ├── README.md              # Documentation index
│   ├── PROJECT_STRUCTURE.md   # Project structure
│   └── MAX_MARKS_UPDATE.md    # Max marks docs
│
├── .github/                    # GitHub configuration
│   └── workflows/             # CI/CD workflows
│
├── run_api.py                  # API entry point
├── run_streamlit.py            # Streamlit entry point
├── requirements.txt            # Python dependencies
├── package.json                # Node.js dependencies
├── prisma.config.ts            # Prisma configuration
├── .env                        # Environment variables (not in repo)
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
│
├── README.md                   # Project overview
├── API_DOCUMENTATION.md        # API reference
├── DEPLOYMENT_GUIDE.md         # Deployment guide
├── PRISMA_SETUP.md             # Prisma setup
├── PRISMA_USAGE_GUIDE.md       # Prisma usage
├── PROJECT_SUMMARY.md          # Quick summary
└── CLEANUP_COMPLETE.md         # Cleanup log
```

## 🎯 Key Directories

### `/src` - Core Application
All main application code lives here:
- **api.py**: FastAPI REST API backend
- **st_main.py**: Streamlit web interface
- **analytics.py**: Advanced analytics engine
- **cgpa_calculator.py**: Grade calculations
- **web_scraper.py**: Portal data scraping
- **config.py**: Application configuration
- **db_utils_*.py**: Database utilities

### `/tests` - Testing & Utilities
Test scripts and data migration tools:
- **test_add_user.py**: Quick test for adding users
- **register_to_prisma.py**: Register with validation
- **migrate_to_prisma.py**: Migrate data between databases

### `/scripts` - CLI Utilities
Command-line tools for management:
- **manage_user.py**: User CRUD operations
- **register_user.py**: User registration
- **update_all.py**: Batch data updates

### `/deployment` - Deployment Files
Everything needed for deployment:
- **Dockerfile**: Container definition
- **docker-compose.yml**: Multi-container setup
- **vercel.json**: Vercel configuration

### `/prisma` - Database Schema
Prisma ORM files:
- **schema.prisma**: Database models
- **migrations/**: Migration history

### `/docs` - Documentation
Project documentation:
- API references
- Setup guides
- Architecture docs

## 🚀 Entry Points

### Run API Backend
```bash
# Method 1: Using entry point
python run_api.py

# Method 2: Using uvicorn directly
uvicorn src.api:app --reload

# Method 3: Using npm script
npm run dev:api
```

### Run Streamlit App
```bash
# Method 1: Using entry point
python run_streamlit.py

# Method 2: Using streamlit directly
streamlit run src/st_main.py

# Method 3: Using npm script
npm run dev:streamlit
```

### Run Prisma Studio
```bash
npm run prisma:studio
```

## 📦 Import Structure

Since all core files are in `/src`, imports are simple:

```python
# In any src/ file
from src import config
import web_scraper
import db_utils_prisma as db_utils
import cgpa_calculator
import analytics
```

## 🔧 Configuration Files

### Root Level
- **.env**: Environment variables (not in repo)
- **.env.example**: Environment template
- **.gitignore**: Git ignore rules
- **requirements.txt**: Python dependencies
- **package.json**: Node.js dependencies
- **prisma.config.ts**: Prisma configuration

### Deployment
- **deployment/Dockerfile**: Container image
- **deployment/docker-compose.yml**: Container orchestration
- **deployment/vercel.json**: Serverless deployment

## 📚 Documentation Files

### Main Docs (Root)
- **README.md**: Project overview
- **API_DOCUMENTATION.md**: Complete API reference
- **DEPLOYMENT_GUIDE.md**: Deployment instructions
- **PRISMA_SETUP.md**: Prisma setup guide
- **PRISMA_USAGE_GUIDE.md**: How to use Prisma
- **PROJECT_SUMMARY.md**: Quick project summary
- **PROJECT_STRUCTURE.md**: This file

### Docs Folder
- **docs/README.md**: Documentation index
- **docs/PROJECT_STRUCTURE.md**: Detailed structure
- **docs/MAX_MARKS_UPDATE.md**: Max marks documentation

## 🎨 Benefits of This Structure

### ✅ Clean Separation
- Core code in `/src`
- Tests in `/tests`
- Scripts in `/scripts`
- Deployment in `/deployment`
- Docs in `/docs`

### ✅ Easy Navigation
- Clear purpose for each directory
- Related files grouped together
- Easy to find what you need

### ✅ Scalable
- Easy to add new modules
- Clear where new files go
- Maintainable structure

### ✅ Professional
- Industry-standard layout
- Easy for new developers
- Clear project organization

## 🔄 Migration Notes

Files were reorganized from flat structure to organized structure:
- Core app files → `/src`
- Test files → `/tests`
- Deployment files → `/deployment`
- Entry points created in root

All imports still work because files in same directory reference each other directly.

## 📝 Development Workflow

1. **Start Development**:
   ```bash
   # Terminal 1: API
   python run_api.py
   
   # Terminal 2: Streamlit
   python run_streamlit.py
   
   # Terminal 3: Prisma Studio
   npm run prisma:studio
   ```

2. **Make Changes**:
   - Edit files in `/src`
   - Both servers auto-reload

3. **Test**:
   ```bash
   python tests/test_add_user.py
   ```

4. **Deploy**:
   ```bash
   docker-compose -f deployment/docker-compose.yml up -d
   ```

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Run API | `python run_api.py` |
| Run Streamlit | `python run_streamlit.py` |
| View Database | `npm run prisma:studio` |
| Test User Creation | `python tests/test_add_user.py` |
| Migrate Data | `python tests/migrate_to_prisma.py` |
| Deploy Docker | `docker-compose -f deployment/docker-compose.yml up` |

---

**Clean, organized, and professional structure! 🎉**
