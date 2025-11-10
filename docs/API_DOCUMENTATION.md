# Contineo Scraper API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently no authentication required. Add JWT/API keys for production.

---

## Endpoints

### Health Check

#### `GET /`
Get API status
```json
{
  "status": "online",
  "message": "Contineo Scraper API",
  "version": "1.0.0"
}
```

#### `GET /health`
Health check endpoint
```json
{
  "status": "healthy",
  "timestamp": "2024-11-11T00:00:00Z"
}
```

---

### User Management

#### `POST /api/users/register`
Register a new user with credential validation

**Request Body:**
```json
{
  "username": "gamer709",
  "full_name": "John Doe",
  "prn": "2021XXXX",
  "dob_day": "15",
  "dob_month": "08",
  "dob_year": "2003"
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "username": "gamer709",
  "full_name": "John Doe"
}
```

**Errors:**
- `400`: Invalid credentials
- `409`: Username or PRN already exists

#### `GET /api/users/{username}`
Get user details

**Response:**
```json
{
  "id": 1,
  "username": "gamer709",
  "full_name": "John Doe",
  "prn": "2021XXXX"
}
```

---

### Data Fetching

#### `POST /api/data/fetch/{username}`
Fetch latest attendance and CIE marks from portal

**Query Parameters:**
- `force_refresh` (optional): boolean

**Response:**
```json
{
  "user": {
    "username": "gamer709",
    "full_name": "John Doe",
    "prn": "2021XXXX"
  },
  "attendance": [
    {
      "subject": "CSC601",
      "percentage": 85
    }
  ],
  "cie_marks": {
    "CSC601": {
      "MSE": 18,
      "TH-ISE1": 45,
      "TH-ISE2": 18,
      "ESE": 35
    }
  },
  "scraped_at": "2024-11-11T00:00:00Z"
}
```

#### `GET /api/data/marks/{username}`
Get stored CIE marks

**Response:**
```json
{
  "username": "gamer709",
  "cie_marks": { ... }
}
```

---

### CGPA/SGPA

#### `GET /api/cgpa/calculate/{username}`
Calculate SGPA from current marks

**Response:**
```json
{
  "sgpa": 8.45,
  "total_credits": 24,
  "total_grade_points": 202.8,
  "subjects": [
    {
      "code": "CSC601",
      "name": "SPCC",
      "credits": 4,
      "marks": 116,
      "max_marks": 100,
      "percentage": 116,
      "grade_point": 10,
      "grade": "O"
    }
  ],
  "grade_distribution": {
    "O": 3,
    "A+": 2,
    "A": 1
  }
}
```

#### `POST /api/cgpa/save-semester/{username}`
Save semester record

**Request Body:**
```json
{
  "semester_number": 7,
  "semester_name": "Semester 7",
  "sgpa": 8.45,
  "total_credits": 24,
  "academic_year": "2024-25"
}
```

#### `GET /api/cgpa/semesters/{username}`
Get all semester records and CGPA

**Response:**
```json
{
  "semester_records": [
    {
      "semester_number": 7,
      "semester_name": "Semester 7",
      "sgpa": 8.45,
      "total_credits": 24,
      "academic_year": "2024-25"
    }
  ],
  "cgpa": {
    "cgpa": 8.12,
    "total_credits": 48,
    "total_grade_points": 389.76
  }
}
```

#### `GET /api/cgpa/target/{username}?target_sgpa=8.5`
Calculate what's needed for target SGPA

**Query Parameters:**
- `target_sgpa`: float (required)

**Response:**
```json
{
  "is_achievable": true,
  "current_sgpa": 8.0,
  "target_sgpa": 8.5,
  "needed_grade_points": 12.0,
  "avg_grade_point_needed": 8.5,
  "recommendations": [
    {
      "subject": "SPCC",
      "code": "CSC601",
      "credits": 4,
      "grade_point_needed": 8.5,
      "minimum_marks_needed": 70,
      "grade_needed": "A"
    }
  ]
}
```

---

### Analytics

#### `GET /api/analytics/performance/{username}`
Subject-wise performance dashboard

**Response:**
```json
{
  "subjects": [
    {
      "code": "CSC601",
      "name": "SPCC",
      "type": "Theory",
      "credits": 4,
      "total_marks": 116,
      "max_marks": 100,
      "percentage": 116,
      "grade": "O",
      "grade_point": 10,
      "completion_rate": 100,
      "completed_exams": ["MSE", "TH-ISE1", "TH-ISE2", "ESE"],
      "pending_exams": [],
      "marks_breakdown": {
        "MSE": 18,
        "TH-ISE1": 45,
        "TH-ISE2": 18,
        "ESE": 35
      }
    }
  ],
  "overall_stats": {
    "average_percentage": 82.5,
    "median_percentage": 85.0,
    "std_deviation": 8.2,
    "highest_percentage": 95.0,
    "lowest_percentage": 68.0,
    "total_subjects": 6
  },
  "weak_subjects": [...],
  "strong_subjects": [...]
}
```

#### `GET /api/analytics/correlation/{username}`
Attendance vs marks correlation analysis

**Response:**
```json
{
  "correlation_coefficient": 0.756,
  "subject_correlations": [
    {
      "subject_code": "CSC601",
      "subject_name": "SPCC",
      "attendance": 85,
      "marks_percentage": 88,
      "difference": 3
    }
  ],
  "insights": [
    "Strong positive correlation: Higher attendance leads to better marks",
    "Excelling in 2 subjects even with lower attendance"
  ],
  "interpretation": "Strong positive correlation"
}
```

#### `GET /api/analytics/semester-comparison/{username}`
Compare performance across semesters

**Response:**
```json
{
  "semester_comparison": [
    {
      "semester_number": 6,
      "semester_name": "Semester 6",
      "sgpa": 7.8,
      "credits": 24,
      "academic_year": "2023-24"
    },
    {
      "semester_number": 7,
      "semester_name": "Semester 7",
      "sgpa": 8.2,
      "credits": 24,
      "academic_year": "2024-25"
    }
  ],
  "trends": {
    "average_sgpa": 8.0,
    "highest_sgpa": 8.2,
    "lowest_sgpa": 7.8,
    "sgpa_range": 0.4,
    "consistency": "High"
  },
  "best_semester": {
    "semester_number": 7,
    "sgpa": 8.2
  },
  "improvement_rate": 0.4,
  "trend_direction": "Improving"
}
```

#### `GET /api/analytics/predictions/{username}`
Predictive analytics for final grades

**Response:**
```json
{
  "predictions": [
    {
      "subject_code": "CSC601",
      "subject_name": "SPCC",
      "current_marks": 76,
      "current_percentage": 76,
      "current_grade": "B+",
      "ese_pending": true,
      "grade_predictions": {
        "O": {
          "ese_marks_needed": 9,
          "achievable": true
        },
        "A+": {
          "ese_marks_needed": 4,
          "achievable": true
        }
      }
    }
  ],
  "current_sgpa": 7.5,
  "recommendations": [
    "You have 3 subjects with ESE pending",
    "Focus on these subjects for easy grade improvements:",
    "  • SPCC: Score 9/40 in ESE for O grade"
  ]
}
```

---

### Leaderboards

#### `GET /api/leaderboard/{subject_code}/{exam_type}?limit=10`
Get leaderboard for subject and exam

**Parameters:**
- `subject_code`: e.g., "CSC601"
- `exam_type`: e.g., "MSE", "TH-ISE1"
- `limit`: number of top students (default: 10)

**Response:**
```json
{
  "subject_code": "CSC601",
  "exam_type": "MSE",
  "leaderboard": [
    {
      "rank": 1,
      "name": "John Doe",
      "marks": 20
    },
    {
      "rank": 2,
      "name": "Jane Smith",
      "marks": 19
    }
  ]
}
```

---

### Configuration

#### `GET /api/config/subjects`
Get all subject mappings and credits

**Response:**
```json
{
  "subjects": {
    "CSC601": "SPCC (System Programming & Compiler Construction)",
    "CSC602": "CSS (Cryptography and System Security)",
    ...
  },
  "credits": {
    "CSC601": 4,
    "CSL601": 2,
    ...
  }
}
```

---

## Error Responses

All endpoints return standard error responses:

```json
{
  "detail": "Error message here"
}
```

**Common Status Codes:**
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `409`: Conflict
- `500`: Internal Server Error

---

## Rate Limiting

Consider implementing rate limiting for production:
- Login/scraping endpoints: 10 requests per minute
- Analytics endpoints: 30 requests per minute
- Other endpoints: 60 requests per minute

---

## Next.js Integration Example

```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchStudentData(username: string) {
  const response = await fetch(`${API_BASE_URL}/api/data/fetch/${username}`, {
    method: 'POST',
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch data');
  }
  
  return response.json();
}

export async function getPerformanceAnalytics(username: string) {
  const response = await fetch(`${API_BASE_URL}/api/analytics/performance/${username}`);
  return response.json();
}

// Usage in component
const { data, error } = useSWR(
  `/api/analytics/performance/${username}`,
  () => getPerformanceAnalytics(username)
);
```

---

## Deployment

### Local Development
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Production (Docker)
See `Dockerfile` and `docker-compose.yml`

### Environment Variables
```env
NEON_DB_PASSWORD=your_password
NEON_DB_URI=your_neon_uri
PG_DBNAME=neondb
PG_USER=neondb_owner
NEON_PASSWORDLESS_AUTH=false
```
