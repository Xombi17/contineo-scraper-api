# cgpa_calculator.py
"""
CGPA/SGPA Calculator Module
Handles grade point calculations, CGPA/SGPA computation, and target grade predictions.
Uses percentage-based pointer system.
"""

from . import config
from . import exam_max_marks

# Percentage-based Grade Point System (10-point scale)
# Based on percentage of marks obtained
GRADE_RANGES_PERCENTAGE = [
    (85, 100, 10, 'O'),   # Outstanding - ≥85%
    (80, 84.99, 9, 'A+'), # Excellent - ≥80%
    (70, 79.99, 8, 'A'),  # Very Good - ≥70%
    (60, 69.99, 7, 'B+'), # Good - ≥60%
    (50, 59.99, 6, 'B'),  # Above Average - ≥50%
    (45, 49.99, 5, 'C'),  # Average - ≥45%
    (40, 44.99, 4, 'P'),  # Pass - ≥40%
    (0, 39.99, 0, 'F'),   # Fail - <40%
]

def get_grade_point(marks, max_marks=100):
    """
    Convert marks to grade points based on percentage-based grading system.
    
    Args:
        marks (float/int): Marks obtained
        max_marks (float/int): Maximum marks possible (default: 100)
    
    Returns:
        tuple: (grade_point, grade_letter)
    """
    if marks is None or marks < 0 or max_marks <= 0:
        return 0, 'F'
    
    # Calculate percentage
    percentage = (marks / max_marks) * 100
    
    # Find the grade based on percentage
    for min_percent, max_percent, grade_point, grade_letter in GRADE_RANGES_PERCENTAGE:
        if min_percent <= percentage <= max_percent:
            return grade_point, grade_letter
    
    return 0, 'F'


def get_subject_credits(subject_code):
    """
    Get credit hours for a subject based on subject type.
    
    Args:
        subject_code (str): Subject code (e.g., "CSC601", "CSL601")
    
    Returns:
        int: Credit hours for the subject
    """
    # First check if it's in the explicit mapping
    if subject_code in config.SUBJECT_CREDITS:
        return config.SUBJECT_CREDITS[subject_code]
    
    # Otherwise, use pattern-based defaults
    return config.get_default_credits_by_type(subject_code)


def calculate_subject_total(marks_dict, subject_code):
    """
    Calculate total marks and max marks for a subject based on exam components.
    Uses smart inference to determine max marks for each component.
    
    Args:
        marks_dict (dict): Dictionary of exam types and marks (e.g., {"MSE": 15, "TH-ISE1": 48, ...})
        subject_code (str): Subject code to determine calculation method
    
    Returns:
        tuple: (total_marks, max_marks) or (None, None) if no marks available
    """
    total = 0.0
    max_total = 0.0
    has_marks = False
    
    for exam_type, mark in marks_dict.items():
        if isinstance(mark, (int, float)) and mark is not None:
            # Get max marks for this exam type
            max_for_exam = exam_max_marks.get_max_marks_for_exam(subject_code, exam_type)
            
            # If we don't have a configured max, try to infer it from the value
            if max_for_exam is None:
                max_for_exam = exam_max_marks.infer_max_marks_from_value(mark)
            
            total += mark
            max_total += max_for_exam
            has_marks = True
    
    return (total, max_total) if has_marks else (None, None)


def calculate_sgpa(cie_marks_data):
    """
    Calculate SGPA (Semester Grade Point Average) from CIE marks.
    Uses the formula: (totalPoints / (totalCredits * 10)) * 10
    
    Args:
        cie_marks_data (dict): Dictionary of subject codes to marks dictionaries
    
    Returns:
        dict: {
            'sgpa': float,
            'total_credits': int,
            'subjects': list of subject details,
            'grade_distribution': dict of grade counts
        }
    """
    total_points = 0.0  # Sum of (grade_point * credits)
    total_credits = 0
    subjects_info = []
    grade_distribution = {}
    
    for subject_code, marks_dict in cie_marks_data.items():
        # Calculate total marks for the subject
        result = calculate_subject_total(marks_dict, subject_code)
        
        if result != (None, None):
            total_marks, max_marks = result
            
            # Get grade point (out of 10) based on percentage
            grade_point, grade_letter = get_grade_point(total_marks, max_marks=max_marks)
            subject_credits = get_subject_credits(subject_code)
            
            # Add to total points (pointer * credits)
            total_points += grade_point * subject_credits
            total_credits += subject_credits
            
            # Track grade distribution
            grade_distribution[grade_letter] = grade_distribution.get(grade_letter, 0) + 1
            
            # Store subject info
            subject_name = config.SUBJECT_CODE_TO_NAME_MAP.get(subject_code, subject_code)
            percentage = round((total_marks / max_marks) * 100, 2) if max_marks > 0 else 0
            subjects_info.append({
                'code': subject_code,
                'name': subject_name,
                'credits': subject_credits,
                'marks': total_marks,
                'max_marks': max_marks,
                'percentage': percentage,
                'grade_point': grade_point,
                'grade': grade_letter
            })
    
    # Calculate SGPA using formula: (totalPoints / (totalCredits * 10)) * 10
    # This simplifies to: totalPoints / totalCredits
    sgpa = (total_points / (total_credits * 10)) * 10 if total_credits > 0 else 0.0
    
    return {
        'sgpa': round(sgpa, 2),
        'total_credits': total_credits,
        'total_grade_points': round(total_points, 2),
        'subjects': subjects_info,
        'grade_distribution': grade_distribution
    }


def calculate_cgpa(semester_data_list):
    """
    Calculate CGPA (Cumulative Grade Point Average) from multiple semesters.
    Uses the formula: (totalPoints / (totalCredits * 10)) * 10
    
    Args:
        semester_data_list (list): List of SGPA calculation results from different semesters
    
    Returns:
        dict: {
            'cgpa': float,
            'total_credits': int,
            'semesters': list of semester summaries
        }
    """
    total_points = 0.0
    total_credits = 0
    semester_summaries = []
    
    for sem_data in semester_data_list:
        if 'total_grade_points' in sem_data and 'total_credits' in sem_data:
            total_points += sem_data['total_grade_points']
            total_credits += sem_data['total_credits']
            semester_summaries.append({
                'sgpa': sem_data['sgpa'],
                'credits': sem_data['total_credits']
            })
    
    # Calculate CGPA using formula: (totalPoints / (totalCredits * 10)) * 10
    cgpa = (total_points / (total_credits * 10)) * 10 if total_credits > 0 else 0.0
    
    return {
        'cgpa': round(cgpa, 2),
        'total_credits': total_credits,
        'total_grade_points': round(total_points, 2),
        'semesters': semester_summaries
    }


def calculate_required_marks_for_target(current_cie_marks, target_sgpa, subject_priorities=None):
    """
    Calculate how much marks needed in remaining subjects to achieve target SGPA.
    
    Args:
        current_cie_marks (dict): Current CIE marks data
        target_sgpa (float): Desired SGPA to achieve
        subject_priorities (list): Optional list of subject codes to focus on
    
    Returns:
        dict: Analysis of what's needed to achieve target SGPA
    """
    # First, calculate current state
    current_stats = calculate_sgpa(current_cie_marks)
    
    # Identify subjects with incomplete marks
    incomplete_subjects = []
    complete_subjects = []
    
    for subject_code, marks_dict in current_cie_marks.items():
        result = calculate_subject_total(marks_dict, subject_code)
        subject_name = config.SUBJECT_CODE_TO_NAME_MAP.get(subject_code, subject_code)
        credits = get_subject_credits(subject_code)
        
        if result == (None, None):
            # Check what's missing
            missing_exams = []
            if subject_code.startswith("CSC") or subject_code.startswith("CSDC") or \
               subject_code.startswith("25PCC") or subject_code.startswith("25PEC"):
                for exam in ["MSE", "TH-ISE1", "TH-ISE2", "ESE"]:
                    if not isinstance(marks_dict.get(exam), (int, float)):
                        missing_exams.append(exam)
            elif subject_code.startswith("CSL") or subject_code.startswith("CSDL"):
                for exam in ["PR-ISE1", "PR-ISE2"]:
                    if not isinstance(marks_dict.get(exam), (int, float)):
                        missing_exams.append(exam)
            
            incomplete_subjects.append({
                'code': subject_code,
                'name': subject_name,
                'credits': credits,
                'current_marks': marks_dict,
                'missing_exams': missing_exams
            })
        else:
            total_marks, max_marks = result
            complete_subjects.append({
                'code': subject_code,
                'name': subject_name,
                'credits': credits,
                'marks': total_marks,
                'max_marks': max_marks
            })
    
    if not incomplete_subjects:
        return {
            'is_achievable': current_stats['sgpa'] >= target_sgpa,
            'current_sgpa': current_stats['sgpa'],
            'target_sgpa': target_sgpa,
            'message': 'All subjects complete. No exams remaining.',
            'incomplete_subjects': [],
            'recommendations': []
        }
    
    # Calculate total grade points needed
    total_credits_all = sum(s['credits'] for s in complete_subjects) + \
                        sum(s['credits'] for s in incomplete_subjects)
    
    # Using formula: (totalPoints / (totalCredits * 10)) * 10 = target_sgpa
    # So: totalPoints = (target_sgpa * totalCredits * 10) / 10
    # Which simplifies to: totalPoints = target_sgpa * totalCredits
    target_total_grade_points = target_sgpa * total_credits_all
    
    # Grade points already earned from complete subjects
    earned_grade_points = sum(
        get_grade_point(s['marks'], max_marks=100)[0] * s['credits'] 
        for s in complete_subjects
    )
    
    # Grade points needed from incomplete subjects
    needed_grade_points = target_total_grade_points - earned_grade_points
    incomplete_credits = sum(s['credits'] for s in incomplete_subjects)
    
    if incomplete_credits == 0:
        return {
            'is_achievable': False,
            'current_sgpa': current_stats['sgpa'],
            'target_sgpa': target_sgpa,
            'message': 'No incomplete subjects to improve.',
            'incomplete_subjects': incomplete_subjects,
            'recommendations': []
        }
    
    # Average grade point needed per credit in incomplete subjects
    avg_gp_needed = needed_grade_points / incomplete_credits
    
    # Convert grade point to approximate percentage and marks needed
    recommendations = []
    
    for subject in incomplete_subjects:
        gp_needed_for_subject = avg_gp_needed
        
        # Find minimum percentage needed to achieve this grade point
        percentage_needed = None
        grade_needed = None
        
        for min_percent, max_percent, gp, grade in GRADE_RANGES_PERCENTAGE:
            if gp >= gp_needed_for_subject:
                percentage_needed = min_percent
                grade_needed = grade
                break
        
        if percentage_needed is None:
            percentage_needed = 85  # Default to O grade
            grade_needed = 'O'
        
        # Convert percentage to marks out of 100
        marks_needed = percentage_needed  # Since max_marks is 100
        
        recommendations.append({
            'subject': subject['name'],
            'code': subject['code'],
            'credits': subject['credits'],
            'grade_point_needed': round(gp_needed_for_subject, 2),
            'minimum_marks_needed': marks_needed,
            'grade_needed': grade_needed,
            'missing_exams': subject['missing_exams']
        })
    
    is_achievable = avg_gp_needed <= 10  # Maximum grade point is 10
    
    return {
        'is_achievable': is_achievable,
        'current_sgpa': current_stats['sgpa'],
        'target_sgpa': target_sgpa,
        'needed_grade_points': round(needed_grade_points, 2),
        'avg_grade_point_needed': round(avg_gp_needed, 2),
        'incomplete_subjects': incomplete_subjects,
        'recommendations': recommendations,
        'message': 'Target achievable!' if is_achievable else 'Target may not be achievable with remaining subjects.'
    }


def get_grade_summary_text(grade_point):
    """
    Get descriptive text for a grade point.
    
    Args:
        grade_point (float): Grade point value
    
    Returns:
        str: Description of the grade
    """
    if grade_point >= 9:
        return "Excellent! 🌟"
    elif grade_point >= 8:
        return "Very Good! 👏"
    elif grade_point >= 7:
        return "Good 👍"
    elif grade_point >= 6:
        return "Above Average"
    elif grade_point >= 5:
        return "Average"
    else:
        return "Needs Improvement"
