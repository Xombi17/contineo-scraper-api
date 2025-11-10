#!/usr/bin/env python3
"""
Debug CGPA Calculator - Check what's being calculated
"""
import importlib
import db_utils_neon as db_utils  # Changed from db_utils_sqlite to db_utils_neon
import cgpa_calculator
import exam_max_marks

# Force reload modules to get latest changes
importlib.reload(exam_max_marks)
importlib.reload(cgpa_calculator)

# Get user data
username = "xombi7"
user = db_utils.get_user_from_db_pg(username)

if user:
    print(f"Found user: {user['full_name']}")
    print("=" * 70)
    
    # Get CIE marks
    cie_marks = db_utils.get_user_current_cie_marks_pg(user['id'])
    
    print("\nRAW CIE MARKS FROM DATABASE:")
    print("-" * 70)
    for subject_code, marks_dict in cie_marks.items():
        print(f"\n{subject_code}:")
        for exam_type, mark in marks_dict.items():
            print(f"  {exam_type}: {mark}")
    
    print("\n" + "=" * 70)
    print("CALCULATED TOTALS AND MAX MARKS:")
    print("-" * 70)
    
    for subject_code, marks_dict in cie_marks.items():
        result = cgpa_calculator.calculate_subject_total(marks_dict, subject_code)
        if result != (None, None):
            total, max_marks = result
            if total is not None and max_marks is not None and max_marks > 0:
                percentage = (total / max_marks * 100)
                gp, grade = cgpa_calculator.get_grade_point(int(total), int(max_marks))
                print(f"\n{subject_code}:")
                print(f"  Total Marks: {total}")
                print(f"  Max Marks: {max_marks}")
                print(f"  Percentage: {percentage:.2f}%")
                print(f"  Grade: {grade} ({gp} GP)")
            else:
                print(f"\n{subject_code}: Invalid marks data")
        else:
            print(f"\n{subject_code}: No marks available")
    
    print("\n" + "=" * 70)
    print("SGPA CALCULATION:")
    print("-" * 70)
    sgpa_result = cgpa_calculator.calculate_sgpa(cie_marks)
    print(f"SGPA: {sgpa_result['sgpa']}")
    print(f"Total Credits: {sgpa_result['total_credits']}")
    
else:
    print(f"User '{username}' not found")