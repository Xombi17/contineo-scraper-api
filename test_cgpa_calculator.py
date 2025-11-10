# test_cgpa_calculator.py
import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import cgpa_calculator
import config
import db_utils_neon as db_utils  # Changed from db_utils_sqlite to db_utils_neon

class TestCGPACalculator(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Initialize database for testing
        db_utils.create_db_and_table_pg()
        
        # Sample test data
        self.sample_marks_data = {
            "CSC601": {"MSE": 18, "TH-ISE1": 19, "TH-ISE2": 17, "ESE": 36},
            "CSC602": {"MSE": 16, "TH-ISE1": 18, "TH-ISE2": 15, "ESE": 32},
            "CSL601": {"PR-ISE1": 45, "PR-ISE2": 48},
            "CSL602": {"PR-ISE1": 42, "PR-ISE2": 46}
        }
        
        # Expected results for the sample data
        self.expected_sgpa = 8.83  # Based on the calculation logic
        self.expected_total_credits = 12  # 4+4+2+2

    def test_calculate_subject_total_theory(self):
        """Test calculation of total marks for theory subjects."""
        subject_code = "CSC601"
        marks_dict = self.sample_marks_data[subject_code]
        total, max_marks = cgpa_calculator.calculate_subject_total(marks_dict, subject_code)
        
        # For theory: MSE(20) + TH-ISE1(20) + TH-ISE2(20) + ESE(40) = 100
        expected_total = 18 + 19 + 17 + 36  # 90
        expected_max = 100
        
        self.assertEqual(total, expected_total)
        self.assertEqual(max_marks, expected_max)

    def test_calculate_subject_total_lab(self):
        """Test calculation of total marks for lab subjects."""
        subject_code = "CSL601"
        marks_dict = self.sample_marks_data[subject_code]
        total, max_marks = cgpa_calculator.calculate_subject_total(marks_dict, subject_code)
        
        # For lab: PR-ISE1(50) + PR-ISE2(50) = 100
        expected_total = 45 + 48  # 93
        expected_max = 100
        
        self.assertEqual(total, expected_total)
        self.assertEqual(max_marks, expected_max)

    def test_get_grade_point_o_grade(self):
        """Test grade point calculation for O grade (≥85%)."""
        total = 85
        max_marks = 100
        gp, grade = cgpa_calculator.get_grade_point(total, max_marks)
        
        self.assertEqual(gp, 10)
        self.assertEqual(grade, "O")

    def test_get_grade_point_a_plus_grade(self):
        """Test grade point calculation for A+ grade (≥80% but <85%)."""
        total = 82
        max_marks = 100
        gp, grade = cgpa_calculator.get_grade_point(total, max_marks)
        
        self.assertEqual(gp, 9)
        self.assertEqual(grade, "A+")

    def test_get_grade_point_f_grade(self):
        """Test grade point calculation for F grade (<40%)."""
        total = 35
        max_marks = 100
        gp, grade = cgpa_calculator.get_grade_point(total, max_marks)
        
        self.assertEqual(gp, 0)
        self.assertEqual(grade, "F")

    def test_calculate_sgpa(self):
        """Test SGPA calculation."""
        result = cgpa_calculator.calculate_sgpa(self.sample_marks_data)
        
        # Verify the structure of the result
        self.assertIn('sgpa', result)
        self.assertIn('total_credits', result)
        self.assertIn('subjects', result)
        self.assertIn('grade_distribution', result)
        
        # Verify total credits
        self.assertEqual(result['total_credits'], self.expected_total_credits)
        
        # Verify SGPA is a float
        self.assertIsInstance(result['sgpa'], float)
        
        # Verify subject details are provided
        self.assertIsInstance(result['subjects'], list)
        self.assertGreater(len(result['subjects']), 0)

    def test_get_default_credits_by_type(self):
        """Test credit determination by subject type."""
        # Theory subject
        self.assertEqual(config.get_default_credits_by_type("CSC601"), 4)
        
        # Lab subject
        self.assertEqual(config.get_default_credits_by_type("CSL601"), 2)
        
        # Project
        self.assertEqual(config.get_default_credits_by_type("CSM601"), 4)
        
        # Skill-based lab
        self.assertEqual(config.get_default_credits_by_type("CSL605"), 1)

    def test_calculate_sgpa_empty_data(self):
        """Test SGPA calculation with empty data."""
        empty_data = {}
        result = cgpa_calculator.calculate_sgpa(empty_data)
        
        # Should return 0 SGPA and 0 credits for empty data
        self.assertEqual(result['sgpa'], 0.0)
        self.assertEqual(result['total_credits'], 0)
        self.assertEqual(result['subjects'], [])

    def test_calculate_subject_total_none_marks(self):
        """Test subject total calculation with None marks."""
        marks_dict = {"MSE": None, "TH-ISE1": 15}
        total, max_marks = cgpa_calculator.calculate_subject_total(marks_dict, "CSC601")
        
        # Should handle None values gracefully
        self.assertIsNotNone(total)
        self.assertIsNotNone(max_marks)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)