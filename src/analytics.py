"""
Analytics Module for Student Performance Analysis
Provides insights, correlations, and predictions
"""

import config
import cgpa_calculator
from typing import Dict, List, Optional, Tuple
import statistics

def calculate_subject_performance_dashboard(cie_marks_records: Dict) -> Dict:
    """
    Generate comprehensive subject-wise performance metrics.
    
    Returns:
        dict: {
            'subjects': [list of subject performance data],
            'overall_stats': {overall statistics},
            'weak_subjects': [subjects needing attention],
            'strong_subjects': [performing well subjects]
        }
    """
    subjects_data = []
    all_percentages = []
    
    for subject_code, marks_dict in cie_marks_records.items():
        result = cgpa_calculator.calculate_subject_total(marks_dict, subject_code)
        
        if result != (None, None):
            total_marks, max_marks = result
            percentage = (total_marks / max_marks) * 100 if max_marks > 0 else 0
            grade_point, grade = cgpa_calculator.get_grade_point(total_marks, max_marks)
            credits = cgpa_calculator.get_subject_credits(subject_code)
            subject_name = config.SUBJECT_CODE_TO_NAME_MAP.get(subject_code, subject_code)
            
            # Determine subject type
            if subject_code.startswith("CSL") or subject_code.startswith("CSDL"):
                subject_type = "Lab"
            elif subject_code.startswith("CSC") or subject_code.startswith("CSDC"):
                subject_type = "Theory"
            else:
                subject_type = "Other"
            
            # Calculate completion status
            expected_exams = []
            if subject_type == "Theory":
                expected_exams = ["MSE", "TH-ISE1", "TH-ISE2", "ESE"]
            elif subject_type == "Lab":
                expected_exams = ["PR-ISE1", "PR-ISE2"]
            
            completed_exams = [exam for exam in expected_exams if isinstance(marks_dict.get(exam), (int, float))]
            completion_rate = (len(completed_exams) / len(expected_exams) * 100) if expected_exams else 100
            
            subject_info = {
                'code': subject_code,
                'name': subject_name,
                'type': subject_type,
                'credits': credits,
                'total_marks': round(total_marks, 2),
                'max_marks': max_marks,
                'percentage': round(percentage, 2),
                'grade': grade,
                'grade_point': grade_point,
                'completion_rate': round(completion_rate, 2),
                'completed_exams': completed_exams,
                'pending_exams': [e for e in expected_exams if e not in completed_exams],
                'marks_breakdown': {k: v for k, v in marks_dict.items() if isinstance(v, (int, float))}
            }
            
            subjects_data.append(subject_info)
            all_percentages.append(percentage)
    
    # Calculate overall statistics
    if all_percentages:
        overall_stats = {
            'average_percentage': round(statistics.mean(all_percentages), 2),
            'median_percentage': round(statistics.median(all_percentages), 2),
            'std_deviation': round(statistics.stdev(all_percentages), 2) if len(all_percentages) > 1 else 0,
            'highest_percentage': round(max(all_percentages), 2),
            'lowest_percentage': round(min(all_percentages), 2),
            'total_subjects': len(subjects_data)
        }
    else:
        overall_stats = {}
    
    # Identify weak and strong subjects
    if all_percentages:
        avg = statistics.mean(all_percentages)
        weak_subjects = [s for s in subjects_data if s['percentage'] < avg - 5]
        strong_subjects = [s for s in subjects_data if s['percentage'] > avg + 5]
    else:
        weak_subjects = []
        strong_subjects = []
    
    return {
        'subjects': subjects_data,
        'overall_stats': overall_stats,
        'weak_subjects': weak_subjects,
        'strong_subjects': strong_subjects
    }


def calculate_attendance_marks_correlation(attendance_records: List, cie_marks_records: Dict) -> Dict:
    """
    Analyze correlation between attendance and marks performance.
    
    Returns:
        dict: {
            'correlation_coefficient': float,
            'subject_correlations': [list of per-subject correlations],
            'insights': [list of insights]
        }
    """
    correlations = []
    subject_data = []
    
    # Create attendance lookup
    attendance_map = {record['subject']: record['percentage'] for record in attendance_records}
    
    for subject_code, marks_dict in cie_marks_records.items():
        if subject_code not in attendance_map:
            continue
        
        result = cgpa_calculator.calculate_subject_total(marks_dict, subject_code)
        if result == (None, None):
            continue
        
        total_marks, max_marks = result
        marks_percentage = (total_marks / max_marks) * 100 if max_marks > 0 else 0
        attendance_percentage = attendance_map[subject_code]
        
        subject_name = config.SUBJECT_CODE_TO_NAME_MAP.get(subject_code, subject_code)
        
        subject_data.append({
            'subject_code': subject_code,
            'subject_name': subject_name,
            'attendance': attendance_percentage,
            'marks_percentage': round(marks_percentage, 2),
            'difference': round(marks_percentage - attendance_percentage, 2)
        })
        
        correlations.append((attendance_percentage, marks_percentage))
    
    # Calculate Pearson correlation coefficient
    correlation_coefficient = 0
    if len(correlations) > 1:
        x_values = [c[0] for c in correlations]
        y_values = [c[1] for c in correlations]
        
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        sum_y2 = sum(y * y for y in y_values)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) ** 0.5
        
        if denominator != 0:
            correlation_coefficient = numerator / denominator
    
    # Generate insights
    insights = []
    if correlation_coefficient > 0.7:
        insights.append("Strong positive correlation: Higher attendance leads to better marks")
    elif correlation_coefficient > 0.4:
        insights.append("Moderate positive correlation: Attendance impacts performance")
    elif correlation_coefficient > 0:
        insights.append("Weak positive correlation: Attendance has some impact on marks")
    else:
        insights.append("No clear correlation between attendance and marks")
    
    # Find subjects where marks are much lower than attendance
    underperforming = [s for s in subject_data if s['difference'] < -10]
    if underperforming:
        insights.append(f"Underperforming in {len(underperforming)} subjects despite good attendance")
    
    # Find subjects where marks are much higher than attendance
    overperforming = [s for s in subject_data if s['difference'] > 10]
    if overperforming:
        insights.append(f"Excelling in {len(overperforming)} subjects even with lower attendance")
    
    return {
        'correlation_coefficient': round(correlation_coefficient, 3),
        'subject_correlations': subject_data,
        'insights': insights,
        'interpretation': _interpret_correlation(correlation_coefficient)
    }


def compare_semesters(semester_records: List) -> Dict:
    """
    Compare performance across different semesters.
    
    Returns:
        dict: {
            'semester_comparison': [list of semester data],
            'trends': {trend analysis},
            'best_semester': dict,
            'improvement_rate': float
        }
    """
    if not semester_records:
        return {'error': 'No semester records available'}
    
    # Sort by semester number
    sorted_semesters = sorted(semester_records, key=lambda x: x['semester_number'])
    
    semester_comparison = []
    sgpa_values = []
    
    for sem in sorted_semesters:
        if sem['sgpa'] is not None:
            semester_comparison.append({
                'semester_number': sem['semester_number'],
                'semester_name': sem['semester_name'],
                'sgpa': sem['sgpa'],
                'credits': sem['total_credits'],
                'academic_year': sem['academic_year']
            })
            sgpa_values.append(sem['sgpa'])
    
    if not sgpa_values:
        return {'error': 'No SGPA data available'}
    
    # Calculate trends
    trends = {
        'average_sgpa': round(statistics.mean(sgpa_values), 2),
        'highest_sgpa': round(max(sgpa_values), 2),
        'lowest_sgpa': round(min(sgpa_values), 2),
        'sgpa_range': round(max(sgpa_values) - min(sgpa_values), 2),
        'consistency': 'High' if statistics.stdev(sgpa_values) < 0.5 else 'Moderate' if statistics.stdev(sgpa_values) < 1.0 else 'Variable'
    }
    
    # Find best semester
    best_semester = max(semester_comparison, key=lambda x: x['sgpa'])
    
    # Calculate improvement rate (linear regression slope)
    if len(sgpa_values) > 1:
        n = len(sgpa_values)
        x_values = list(range(1, n + 1))
        y_values = sgpa_values
        
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(y_values)
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        improvement_rate = numerator / denominator if denominator != 0 else 0
        
        trend_direction = 'Improving' if improvement_rate > 0.1 else 'Declining' if improvement_rate < -0.1 else 'Stable'
    else:
        improvement_rate = 0
        trend_direction = 'Insufficient data'
    
    return {
        'semester_comparison': semester_comparison,
        'trends': trends,
        'best_semester': best_semester,
        'improvement_rate': round(improvement_rate, 3),
        'trend_direction': trend_direction
    }


def predict_final_grades(cie_marks_records: Dict, semester_records: List = None) -> Dict:
    """
    Predict final grades and provide recommendations.
    
    Returns:
        dict: {
            'predictions': [list of subject predictions],
            'overall_prediction': dict,
            'recommendations': [list of actionable recommendations]
        }
    """
    predictions = []
    
    for subject_code, marks_dict in cie_marks_records.items():
        result = cgpa_calculator.calculate_subject_total(marks_dict, subject_code)
        
        if result != (None, None):
            total_marks, max_marks = result
            current_percentage = (total_marks / max_marks) * 100 if max_marks > 0 else 0
            grade_point, grade = cgpa_calculator.get_grade_point(total_marks, max_marks)
            subject_name = config.SUBJECT_CODE_TO_NAME_MAP.get(subject_code, subject_code)
            
            # Check if ESE is pending
            has_ese = isinstance(marks_dict.get('ESE'), (int, float))
            
            if not has_ese and (subject_code.startswith('CSC') or subject_code.startswith('CSDC')):
                # Predict ESE needed for different grades
                current_marks = total_marks
                
                predictions_for_grades = {}
                for target_grade, target_gp in [('O', 10), ('A+', 9), ('A', 8), ('B+', 7)]:
                    # Find minimum percentage for this grade
                    min_percentage = None
                    for min_p, max_p, gp, g in cgpa_calculator.GRADE_RANGES_PERCENTAGE:
                        if g == target_grade:
                            min_percentage = min_p
                            break
                    
                    if min_percentage:
                        required_total = (min_percentage / 100) * 100  # Out of 100
                        ese_needed = required_total - current_marks
                        
                        if ese_needed <= 40:  # ESE is out of 40
                            predictions_for_grades[target_grade] = {
                                'ese_marks_needed': max(0, round(ese_needed, 1)),
                                'achievable': ese_needed <= 40
                            }
                
                predictions.append({
                    'subject_code': subject_code,
                    'subject_name': subject_name,
                    'current_marks': round(current_marks, 2),
                    'current_percentage': round(current_percentage, 2),
                    'current_grade': grade,
                    'ese_pending': True,
                    'grade_predictions': predictions_for_grades
                })
            else:
                # Already complete
                predictions.append({
                    'subject_code': subject_code,
                    'subject_name': subject_name,
                    'current_marks': round(total_marks, 2),
                    'current_percentage': round(current_percentage, 2),
                    'final_grade': grade,
                    'grade_point': grade_point,
                    'ese_pending': False
                })
    
    # Overall prediction
    current_sgpa = cgpa_calculator.calculate_sgpa(cie_marks_records)
    
    # Generate recommendations
    recommendations = _generate_recommendations(predictions, current_sgpa)
    
    return {
        'predictions': predictions,
        'current_sgpa': current_sgpa['sgpa'],
        'recommendations': recommendations
    }


def _interpret_correlation(coefficient: float) -> str:
    """Interpret correlation coefficient"""
    abs_coef = abs(coefficient)
    if abs_coef > 0.7:
        strength = "Strong"
    elif abs_coef > 0.4:
        strength = "Moderate"
    elif abs_coef > 0.2:
        strength = "Weak"
    else:
        strength = "Very weak or no"
    
    direction = "positive" if coefficient > 0 else "negative"
    return f"{strength} {direction} correlation"


def _generate_recommendations(predictions: List, current_sgpa: Dict) -> List[str]:
    """Generate actionable recommendations based on predictions"""
    recommendations = []
    
    # Check for subjects with ESE pending
    pending_subjects = [p for p in predictions if p.get('ese_pending', False)]
    
    if pending_subjects:
        recommendations.append(f"You have {len(pending_subjects)} subjects with ESE pending")
        
        # Find subjects where high grades are achievable
        easy_targets = []
        for subj in pending_subjects:
            if 'grade_predictions' in subj:
                for grade, pred in subj['grade_predictions'].items():
                    if pred['achievable'] and pred['ese_marks_needed'] < 30:
                        easy_targets.append((subj['subject_name'], grade, pred['ese_marks_needed']))
        
        if easy_targets:
            recommendations.append(f"Focus on these subjects for easy grade improvements:")
            for name, grade, marks in easy_targets[:3]:
                recommendations.append(f"  • {name}: Score {marks:.0f}/40 in ESE for {grade} grade")
    
    # SGPA-based recommendations
    if current_sgpa['sgpa'] < 6.0:
        recommendations.append("⚠️ Current SGPA is below 6.0. Focus on improving weak subjects")
    elif current_sgpa['sgpa'] < 7.0:
        recommendations.append("📚 Aim for 7.0+ SGPA by scoring well in remaining exams")
    elif current_sgpa['sgpa'] < 8.0:
        recommendations.append("🎯 You're doing well! Target 8.0+ for excellent performance")
    else:
        recommendations.append("🌟 Excellent performance! Maintain this momentum")
    
    return recommendations
