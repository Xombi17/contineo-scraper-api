"""
FastAPI Backend for Contineo Scraper
REST API for Next.js frontend
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

import web_scraper
import db_utils_neon as db_utils
import cgpa_calculator
import analytics
import config

app = FastAPI(
    title="Contineo Scraper API",
    description="Backend API for student portal data scraping and analytics",
    version="1.0.0"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Add your Next.js URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserRegistration(BaseModel):
    username: str
    full_name: str
    prn: str
    dob_day: str
    dob_month: str
    dob_year: str

class UserLogin(BaseModel):
    username: str

class SemesterRecord(BaseModel):
    semester_number: int
    semester_name: str
    sgpa: float
    total_credits: int
    academic_year: Optional[str] = None

# Initialize database
@app.on_event("startup")
async def startup_event():
    db_utils.create_db_and_table_pg()

# Health check
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Contineo Scraper API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(pytz.utc).isoformat()}

# User Management Endpoints
@app.post("/api/users/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegistration):
    """Register a new user with credential validation"""
    
    # Validate credentials by attempting login
    _, validation_html = web_scraper.login_and_get_welcome_page(
        user.prn, user.dob_day, user.dob_month, user.dob_year, user.full_name
    )
    
    if not validation_html:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials. Please check PRN, DOB, and Full Name"
        )
    
    # Add to database
    success = db_utils.add_user_to_db_pg(
        user.username, user.full_name, user.prn,
        user.dob_day, user.dob_month, user.dob_year
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or PRN already exists"
        )
    
    return {
        "message": "User registered successfully",
        "username": user.username,
        "full_name": user.full_name
    }

@app.get("/api/users/{username}")
async def get_user(username: str):
    """Get user details by username"""
    user_details = db_utils.get_user_from_db_pg(username)
    
    if not user_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{username}' not found"
        )
    
    return {
        "id": user_details["id"],
        "username": username,
        "full_name": user_details["full_name"],
        "prn": user_details["prn"]
    }

# Data Fetching Endpoints
@app.post("/api/data/fetch/{username}")
async def fetch_student_data(username: str, force_refresh: bool = False):
    """Fetch attendance and CIE marks for a user"""
    
    # Get user details
    user_details = db_utils.get_user_from_db_pg(username)
    if not user_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{username}' not found"
        )
    
    # Login and scrape data
    session, html = web_scraper.login_and_get_welcome_page(
        user_details["prn"],
        user_details["dob_day"],
        user_details["dob_month"],
        user_details["dob_year"],
        user_details["full_name"]
    )
    
    if not html:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to login to portal"
        )
    
    # Extract data
    attendance_records = web_scraper.extract_attendance_from_welcome_page(html)
    cie_marks_records = web_scraper.extract_cie_marks(html)
    
    # Update database
    scraped_at = datetime.now(pytz.utc)
    if cie_marks_records:
        db_utils.update_student_marks_in_db_pg(
            user_details["id"],
            cie_marks_records,
            scraped_at
        )
    
    return {
        "user": {
            "username": username,
            "full_name": user_details["full_name"],
            "prn": user_details["prn"]
        },
        "attendance": attendance_records,
        "cie_marks": cie_marks_records,
        "scraped_at": scraped_at.isoformat()
    }

@app.get("/api/data/attendance/{username}")
async def get_attendance(username: str):
    """Get attendance data for a user"""
    user_details = db_utils.get_user_from_db_pg(username)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    
    # This would need to be cached or fetched from DB
    # For now, we'll return a message to use /fetch endpoint
    return {
        "message": "Use /api/data/fetch/{username} to get latest data"
    }

@app.get("/api/data/marks/{username}")
async def get_marks(username: str):
    """Get CIE marks for a user"""
    user_details = db_utils.get_user_from_db_pg(username)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    
    cie_marks = db_utils.get_user_current_cie_marks_pg(user_details["id"])
    
    return {
        "username": username,
        "cie_marks": cie_marks
    }

# CGPA/SGPA Endpoints
@app.get("/api/cgpa/calculate/{username}")
async def calculate_sgpa(username: str):
    """Calculate SGPA from current CIE marks"""
    user_details = db_utils.get_user_from_db_pg(username)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    
    cie_marks = db_utils.get_user_current_cie_marks_pg(user_details["id"])
    
    if not cie_marks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No marks data available"
        )
    
    sgpa_result = cgpa_calculator.calculate_sgpa(cie_marks)
    
    return sgpa_result

@app.post("/api/cgpa/save-semester/{username}")
async def save_semester(username: str, semester: SemesterRecord):
    """Save semester record for CGPA tracking"""
    user_details = db_utils.get_user_from_db_pg(username)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    
    success = db_utils.save_semester_record_pg(
        user_details["id"],
        semester.semester_number,
        semester.semester_name,
        semester.sgpa,
        semester.total_credits,
        semester.academic_year
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save semester record"
        )
    
    return {"message": "Semester record saved successfully"}

@app.get("/api/cgpa/semesters/{username}")
async def get_semesters(username: str):
    """Get all semester records for a user"""
    user_details = db_utils.get_user_from_db_pg(username)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    
    semester_records = db_utils.get_user_semester_records_pg(user_details["id"])
    
    # Calculate CGPA if records exist
    cgpa_data = None
    if semester_records:
        semester_data_for_cgpa = []
        for sem in semester_records:
            if sem['sgpa'] is not None:
                semester_data_for_cgpa.append({
                    'sgpa': sem['sgpa'],
                    'total_credits': sem['total_credits'],
                    'total_grade_points': sem['sgpa'] * sem['total_credits']
                })
        
        if semester_data_for_cgpa:
            cgpa_data = cgpa_calculator.calculate_cgpa(semester_data_for_cgpa)
    
    return {
        "semester_records": semester_records,
        "cgpa": cgpa_data
    }

@app.get("/api/cgpa/target/{username}")
async def calculate_target(username: str, target_sgpa: float):
    """Calculate what's needed to achieve target SGPA"""
    user_details = db_utils.get_user_from_db_pg(username)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    
    cie_marks = db_utils.get_user_current_cie_marks_pg(user_details["id"])
    
    if not cie_marks:
        raise HTTPException(status_code=404, detail="No marks data available")
    
    target_analysis = cgpa_calculator.calculate_required_marks_for_target(
        cie_marks,
        target_sgpa
    )
    
    return target_analysis

# Analytics Endpoints
@app.get("/api/analytics/performance/{username}")
async def get_performance_dashboard(username: str):
    """Get comprehensive subject-wise performance analysis"""
    user_details = db_utils.get_user_from_db_pg(username)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    
    cie_marks = db_utils.get_user_current_cie_marks_pg(user_details["id"])
    
    if not cie_marks:
        raise HTTPException(status_code=404, detail="No marks data available")
    
    performance_data = analytics.calculate_subject_performance_dashboard(cie_marks)
    
    return performance_data

@app.get("/api/analytics/correlation/{username}")
async def get_attendance_correlation(username: str):
    """Analyze correlation between attendance and marks"""
    user_details = db_utils.get_user_from_db_pg(username)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Need to fetch fresh data for attendance
    session, html = web_scraper.login_and_get_welcome_page(
        user_details["prn"],
        user_details["dob_day"],
        user_details["dob_month"],
        user_details["dob_year"],
        user_details["full_name"]
    )
    
    if not html:
        raise HTTPException(status_code=401, detail="Failed to fetch data")
    
    attendance_records = web_scraper.extract_attendance_from_welcome_page(html)
    cie_marks = db_utils.get_user_current_cie_marks_pg(user_details["id"])
    
    if not attendance_records or not cie_marks:
        raise HTTPException(status_code=404, detail="Insufficient data for correlation")
    
    correlation_data = analytics.calculate_attendance_marks_correlation(
        attendance_records,
        cie_marks
    )
    
    return correlation_data

@app.get("/api/analytics/semester-comparison/{username}")
async def compare_semesters(username: str):
    """Compare performance across semesters"""
    user_details = db_utils.get_user_from_db_pg(username)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    
    semester_records = db_utils.get_user_semester_records_pg(user_details["id"])
    
    if not semester_records:
        raise HTTPException(status_code=404, detail="No semester records available")
    
    comparison_data = analytics.compare_semesters(semester_records)
    
    return comparison_data

@app.get("/api/analytics/predictions/{username}")
async def get_grade_predictions(username: str):
    """Get predictive analytics for final grades"""
    user_details = db_utils.get_user_from_db_pg(username)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    
    cie_marks = db_utils.get_user_current_cie_marks_pg(user_details["id"])
    semester_records = db_utils.get_user_semester_records_pg(user_details["id"])
    
    if not cie_marks:
        raise HTTPException(status_code=404, detail="No marks data available")
    
    predictions = analytics.predict_final_grades(cie_marks, semester_records)
    
    return predictions

# Leaderboard Endpoints
@app.get("/api/leaderboard/{subject_code}/{exam_type}")
async def get_leaderboard(subject_code: str, exam_type: str, limit: int = 10):
    """Get leaderboard for a specific subject and exam type"""
    leaderboard = db_utils.get_subject_leaderboard_pg(subject_code, exam_type, limit)
    
    if not leaderboard:
        raise HTTPException(
            status_code=404,
            detail=f"No leaderboard data for {subject_code} - {exam_type}"
        )
    
    return {
        "subject_code": subject_code,
        "exam_type": exam_type,
        "leaderboard": [
            {"rank": idx + 1, "name": name, "marks": marks}
            for idx, (name, marks) in enumerate(leaderboard)
        ]
    }

# Subject Configuration
@app.get("/api/config/subjects")
async def get_subjects():
    """Get all subject mappings"""
    return {
        "subjects": config.SUBJECT_CODE_TO_NAME_MAP,
        "credits": config.SUBJECT_CREDITS
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
