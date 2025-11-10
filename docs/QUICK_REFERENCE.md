# CGPA Calculator - Quick Reference Cheat Sheet

## 🚀 Quick Commands

```bash
# Run the web app
streamlit run st_main.py

# Run tests
python test_cgpa_calculator.py

# Run CLI version
python main.py

# Batch update all students
python update_all.py
```

---

## 📊 Grade Point Scale (Percentage-Based)

| Percentage | Grade | GP | Description |
|-----------|-------|-----|-------------|
| ≥85% | O | 10 | Outstanding ⭐ |
| ≥80% | A+ | 9 | Excellent 🌟 |
| ≥70% | A | 8 | Very Good 👏 |
| ≥60% | B+ | 7 | Good 👍 |
| ≥50% | B | 6 | Above Avg |
| ≥45% | C | 5 | Average |
| ≥40% | P | 4 | Pass |
| <40% | F | 0 | Fail ❌ |

---

## 🧮 Formula Reference

### SGPA (Semester Grade Point Average)
```
Step 1: Calculate percentage for each subject
Percentage = (Obtained Marks / Max Marks) * 100

Step 2: Get grade point based on percentage (see table above)

Step 3: Calculate total points
Total Points = Σ(Grade Point × Credits)

Step 4: Calculate SGPA
SGPA = (Total Points / (Total Credits × 10)) × 10
     = Total Points / Total Credits  (simplified)
```

### CGPA (Cumulative Grade Point Average)
```
CGPA = (All Semester Total Points / (All Credits × 10)) × 10
     = All Semester Total Points / All Credits  (simplified)
```

### Subject Total Marks

**Theory Subjects:**
```
Total = MSE(20) + TH-ISE1(20) + TH-ISE2(20) + ESE(40) = 100
```

**Lab Subjects:**
```
Total = PR-ISE1(50) + PR-ISE2(50) = 100
```

---

## 💾 Credit Hours Quick Reference

| Subject Type | Credits |
|-------------|---------|
| Theory (CSC, BSC, PCC) | 4 |
| Lab (CSL, PECL) | 2 |
| Elective (CSDC, OE) | 3 |
| Project (CSM, CSP) | 4-8 |
| Skill Lab | 1 |

---

## 🎯 Using the Calculator - 3 Steps

### Step 1️⃣: Current SGPA
1. Fetch your data
2. View your SGPA, credits, and grades
3. Save semester record (optional)

### Step 2️⃣: CGPA Tracker
1. See your overall CGPA
2. View semester history
3. Track progress over time

### Step 3️⃣: Target Calculator
1. Enter target SGPA (e.g., 8.5)
2. Click "Calculate Required Marks"
3. See what you need in each subject

---

## 📝 Common Calculations

### Example 1: Calculate SGPA for One Subject
```
Subject: ML (CSC701) - 4 credits
Marks: MSE(18) + ISE1(17) + ISE2(16) + ESE(35) = 86/100
Percentage: 86%
Grade: O (10 GP) [since ≥85%]
Contribution: 10 × 4 = 40 grade points
```

### Example 2: Calculate Full Semester SGPA
```
Subject 1: 4 credits, 86/100 (86%) → 10 GP → 40 points
Subject 2: 4 credits, 77/100 (77%) → 8 GP  → 32 points
Subject 3: 2 credits, 87/100 (87%) → 10 GP → 20 points
Subject 4: 2 credits, 65/100 (65%) → 7 GP  → 14 points
Subject 5: 3 credits, 82/100 (82%) → 9 GP  → 27 points

Total: 15 credits, 133 points
SGPA = (133 / (15 × 10)) × 10 = 133 / 15 = 8.87
```

### Example 3: Target Calculator
```
Current SGPA: 8.0
Target SGPA: 8.5
Incomplete subjects: 2 (8 credits)
Complete subjects grade points: 70 (from 10 credits)

Total needed = 8.5 × 18 = 153
Already have = 70
Need from incomplete = 153 - 70 = 83
Average GP needed = 83 ÷ 8 = 10.375 (Impossible!)

Realistic target: 8.2
```

---

## 🎓 Quick Tips

### Before Exams
✅ Use target calculator to set goals  
✅ Focus on high-credit subjects first  
✅ Know grade boundaries (60 for A+, 70 for O)  

### After Results
✅ Fetch latest data immediately  
✅ Save semester record  
✅ Review grade distribution  

### General
✅ Update data after each exam  
✅ Track trends in CGPA tracker  
✅ Set realistic targets (±0.5 from current SGPA)  

---

## 🔧 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| No SGPA showing | Click "Fetch Data" first |
| "Not achievable" message | Lower your target SGPA |
| Missing subjects | Some exams not conducted yet |
| CGPA shows 0.00 | Save at least one semester record |
| Wrong credits | Check config.py for subject mapping |

---

## 📱 Navigation Map

```
Streamlit App
│
├── Sidebar
│   ├── Username Input
│   ├── Fetch Data Button
│   ├── Get Live Data Button
│   └── Register New Student
│
└── Main Area
    ├── Attendance Data
    ├── CIE Marks & Leaderboards
    └── CGPA/SGPA Calculator ⭐
        ├── Tab 1: Current SGPA
        │   ├── Metrics (SGPA, Credits, Performance)
        │   ├── Grade Distribution
        │   ├── Subject Breakdown
        │   └── Save Semester Form
        │
        ├── Tab 2: CGPA Tracker
        │   ├── Overall CGPA Metrics
        │   └── Semester History Table
        │
        └── Tab 3: Target Calculator
            ├── Target Input
            ├── Calculate Button
            ├── Feasibility Status
            └── Recommendations
```

---

## 💡 Pro Strategies

### To Get 9+ SGPA:
- Need mostly A+ (60+) and O grades (70+)
- Focus on theory subjects (4 credits each)
- Don't neglect labs - easy O grades

### To Improve CGPA:
- Excel in remaining semesters
- Higher SGPA in later semesters helps more
- Each semester matters!

### To Achieve Target:
- Calculate early (before ESE)
- Prioritize subjects with pending exams
- Be strategic with effort allocation

---

## 🎯 Grade Boundaries to Remember

| Want Grade | Need Percentage | Safe Score (out of 100) |
|-----------|----------------|------------------------|
| O | ≥85% | 85+ |
| A+ | ≥80% | 80+ |
| A | ≥70% | 70+ |
| B+ | ≥60% | 60+ |
| B | ≥50% | 50+ |
| C | ≥45% | 45+ |
| P | ≥40% | 40+ |

**Pro Tip:** Always aim 3-5% above the boundary to be safe!

---

## 📞 Need More Help?

1. Check `README.md` - Technical details
2. Run `python test_cgpa_calculator.py` - Verify setup

---

## 🎉 Remember

- **SGPA** = One semester's performance
- **CGPA** = All semesters combined
- **Target Calc** = Planning tool for goals
- **Save Records** = Track your journey!

---

**Good luck with your studies! 🎓📚**

*Keep calm and calculate on!* 🧮✨
