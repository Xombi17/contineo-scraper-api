# Contineo Scraper API

## Overview
A FastAPI backend for scraping student portal data, calculating CGPA/SGPA, and providing analytics. Designed to be consumed by a Next.js frontend.

### Key Features
- 🔐 User registration with credential validation
- 📊 Automated data scraping (attendance & CIE marks)
- 🎓 CGPA/SGPA calculation engine
- 📈 Advanced analytics (performance dashboard, correlations, predictions)
- 🏆 Subject-wise leaderboards
- 🚀 RESTful API ready for Next.js integration

## ✨ API Features

### 1. **User Management**
- Register with credential validation
- Secure storage in Neon PostgreSQL
- User lookup by username

### 2. **Data Scraping**
- Automated login to Contineo portal
- Extract attendance percentages
- Extract CIE marks (MSE, ISE1, ISE2, ESE)
- Real-time data fetching

### 3. **CGPA/SGPA Calculator**
- Calculate current semester SGPA
- Track CGPA across multiple semesters
- Target SGPA calculator with recommendations
- Grade distribution analysis

### 4. **Analytics Engine** 🆕
- **Subject Performance Dashboard**: Comprehensive metrics per subject
- **Attendance-Marks Correlation**: Statistical analysis with insights
- **Semester Comparison**: Trend analysis and improvement tracking
- **Grade Predictions**: Predict final grades and ESE requirements

### 5. **Leaderboards**
- Subject-wise rankings
- Exam-type specific leaderboards
- Top performers tracking

### Grade Point System
Percentage-based 10-point scale:
- **O**: ≥85% → 10 GP
- **A+**: ≥80% → 9 GP
- **A**: ≥70% → 8 GP
- **B+**: ≥60% → 7 GP
- **B**: ≥50% → 6 GP
- **C**: ≥45% → 5 GP
- **P**: ≥40% → 4 GP
- **F**: <40% → 0 GP

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd contineo-scraper

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Neon credentials
```

### Environment Variables
Create a `.env` file:
```env
NEON_DB_PASSWORD=your_password
NEON_DB_URI=ep-xxxxx.region.aws.neon.tech
PG_DBNAME=neondb
PG_USER=neondb_owner
NEON_PASSWORDLESS_AUTH=false
```

### Running the API

#### Development
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

#### Production (Docker)
```bash
docker-compose up -d
```

#### Production (Manual)
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Documentation
Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Or see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for detailed endpoint docs.

## 📊 How to Use the CGPA Calculator

### Step 1: Fetch Your Data
1. Enter your username in the sidebar
2. Click "Fetch Data" to retrieve your marks from Contineo
3. Your attendance and CIE marks will be displayed

### Step 2: View Current SGPA
1. Navigate to the "Current SGPA" tab
2. See your calculated SGPA, credits earned, and grade distribution
3. Review subject-wise performance
4. Save your semester record for CGPA tracking

### Step 3: Track Your CGPA
1. Go to the "CGPA Tracker" tab
2. View your overall CGPA and semester-wise records
3. See how your performance has evolved

### Step 4: Plan for Target SGPA
1. Open the "Target Calculator" tab
2. Enter your desired target SGPA (e.g., 8.5)
3. Click "Calculate Required Marks"
4. See recommendations for each subject:
   - Minimum marks needed
   - Target grade required
   - Grade points needed

## 🗄️ Database Schema

### Tables
- **users**: Student credentials and information
- **cie_marks**: CIE marks for leaderboards and calculations
- **semester_records**: Saved semester data for CGPA tracking

## 📁 Project Structure
```
contineo-scraper/
├── main.py                  # CLI application
├── st_main.py              # Streamlit web interface
├── web_scraper.py          # Web scraping logic
├── db_utils_neon.py        # Neon PostgreSQL database operations
├── cgpa_calculator.py      # CGPA/SGPA calculation engine (NEW!)
├── config.py               # Configuration and subject mappings
├── exam_max_marks.py       # Exam maximum marks configuration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repository)
├── README.md               # This file
├── docs/                   # Documentation files
│   ├── CLEANUP_SUMMARY.md
│   ├── MAX_MARKS_UPDATE.md
│   ├── PROJECT_STRUCTURE.md
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

## 🔧 Configuration

### Subject Credits
Credits are configured in `config.py`:
- Theory subjects: 4 credits
- Lab subjects: 2 credits
- Projects: 4-8 credits
- Skill-based labs: 1 credit

### Customization
You can modify:
- Grade point ranges in `cgpa_calculator.py`
- Subject credit mappings in `config.py`
- Database connection in `.env` file

## 💡 Tips
- Save your semester records regularly to track CGPA over time
- Use the target calculator before exams to plan your preparation
- Check the leaderboard to see how you compare with peers
- The system calculates based on complete exam data - incomplete subjects won't affect SGPA

## 🛠️ Technologies Used
- **Python 3.x**
- **Streamlit**: Web interface
- **BeautifulSoup4**: Web scraping
- **Neon PostgreSQL**: Cloud database
- **Requests**: HTTP client
- **python-dotenv**: Environment management

## 📝 Notes
- Marks are calculated as: MSE + ISE1 + ISE2 + ESE = 100 (for theory)
- Lab subjects: PR-ISE1 + PR-ISE2 = 100
- SGPA is calculated using: (Sum of Grade Points × Credits) / Total Credits
- All data is cached for 1 hour to reduce server load

## 🤝 Contributing
Feel free to contribute by:
- Adding new features
- Improving calculations
- Fixing bugs
- Enhancing UI/UX

## ⚠️ Disclaimer
This tool is for educational purposes. Always verify your grades and CGPA with official university records.