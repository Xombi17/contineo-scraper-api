# Contineo Scraper with CGPA/SGPA Calculator

## Overview
To log into Contineo, we need to input our PRN and DOB, which is annoying when you have to do it every time.

So here you basically register with your PRN and DOB once along with a username (that you will use to get your data).

After registering, you just have to enter the username and your PRN and DOB will automatically be filled in the actual Contineo site and the results will be displayed here (attendance and marks).

## ✨ Features

### 1. **Auto-Login System**
- Register once with your PRN and Date of Birth
- Quick access using just your username
- Secure credential storage in PostgreSQL database

### 2. **Data Scraping**
- **Attendance Tracking**: View attendance percentage for all subjects
- **CIE Marks**: See all your Continuous Internal Evaluation scores
- **Leaderboards**: Compare your performance with other students

### 3. **🎯 CGPA/SGPA Calculator** (NEW!)

#### Current SGPA Calculator
- Automatically calculates your current semester SGPA
- Grade distribution visualization
- Subject-wise breakdown with grade points
- Save semester records for future reference

#### CGPA Tracker
- Track your cumulative GPA across all semesters
- View semester-wise performance history
- Overall performance summary

#### Target Calculator
- Set a target SGPA you want to achieve
- Get recommendations on what marks you need in remaining subjects
- See which exams are pending and how much you need to score
- Grade-wise breakdown for each subject

### 4. **Grade Point System**
Based on percentage-based 10-point grading scale:
- **O (Outstanding)**: ≥85% → 10 GP
- **A+ (Excellent)**: ≥80% → 9 GP
- **A (Very Good)**: ≥70% → 8 GP
- **B+ (Good)**: ≥60% → 7 GP
- **B (Above Average)**: ≥50% → 6 GP
- **C (Average)**: ≥45% → 5 GP
- **P (Pass)**: ≥40% → 4 GP
- **F (Fail)**: <40% → 0 GP

## 🚀 Getting Started

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd contineo-scraper

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with your database credentials
```

### Running the App

#### Streamlit Web Interface (Recommended)
```bash
streamlit run st_main.py
```

#### Command Line Interface
```bash
python main.py
```

#### Batch Update (Update all students)
```bash
python update_all.py
```

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
├── db_utils.py             # Database operations
├── cgpa_calculator.py      # CGPA/SGPA calculation engine (NEW!)
├── config.py               # Configuration and subject mappings
├── update_all.py           # Batch update script
├── requirements.txt        # Python dependencies
└── README.md              # This file
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
- **PostgreSQL**: Database (hosted on Neon.tech)
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
