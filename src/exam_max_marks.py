# exam_max_marks.py
"""
Configuration for maximum marks for each exam type.
Update these values based on your university's marking scheme.
"""

# Default maximum marks for each exam type
# DISABLED - We now infer max marks from actual values for better accuracy
# These are kept for reference only
EXAM_TYPE_MAX_MARKS_REFERENCE = {
    # Theory Exams
    "MSE": 20,           # Mid Semester Exam (can be 20, 25, 30, 40)
    "TH-ISE1": 50,       # Theory ISE 1 (can be 20 or 50 depending on subject)
    "TH-ISE2": 20,       # Theory ISE 2
    "ESE": 40,           # End Semester Exam
    
    # Practical/Lab Exams
    "PR-ISE1": 50,       # Practical ISE 1
    "PR-ISE2": 50,       # Practical ISE 2
    
    # Project/Assignment
    "PROJECT": 100,
    "ASSIGNMENT": 50,
}

# Subject-specific overrides
# Use this if a particular subject has different max marks than default
SUBJECT_SPECIFIC_MAX_MARKS = {
    # Example format:
    # "25VEC12CE01": {
    #     "TH-ISE1": 50,  # This subject's TH-ISE1 is out of 50 instead of 20
    # },
    # Add your subjects here as you discover their max marks
}

def get_max_marks_for_exam(subject_code, exam_type):
    """
    Get maximum marks for a specific exam type in a subject.
    
    Args:
        subject_code (str): Subject code
        exam_type (str): Exam type (e.g., "MSE", "TH-ISE1")
    
    Returns:
        int/float: Maximum marks for that exam, or None if unknown
    """
    # Check subject-specific override first
    if subject_code in SUBJECT_SPECIFIC_MAX_MARKS:
        if exam_type in SUBJECT_SPECIFIC_MAX_MARKS[subject_code]:
            return SUBJECT_SPECIFIC_MAX_MARKS[subject_code][exam_type]
    
    # Return None so caller will infer from actual marks
    return None


def infer_max_marks_from_value(marks_value):
    """
    Try to infer maximum marks based on the actual marks obtained.
    This is a heuristic approach when we don't know the exact max.
    Uses a smart ceiling approach - finds the next "round" number above the marks.
    
    Args:
        marks_value (float): The marks obtained
    
    Returns:
        float: Likely maximum marks
    """
    # Round up to nearest common max value
    # Common max marks: 20, 25, 40, 50, 60, 75, 100
    
    if marks_value <= 20:
        return 20
    elif marks_value <= 25:
        return 25
    elif marks_value <= 30:
        return 30
    elif marks_value <= 40:
        return 40
    elif marks_value <= 50:
        return 50
    elif marks_value <= 60:
        return 60
    elif marks_value <= 75:
        return 75
    elif marks_value <= 100:
        return 100
    else:
        # If marks > 100, round up to nearest 50
        return ((int(marks_value) // 50) + 1) * 50
