# Contineo Scraper API - Project Summary

## 🎯 What This Project Does

A **FastAPI backend** that scrapes student portal data, calculates CGPA/SGPA, and provides advanced analytics. Designed to be consumed by a Next.js frontend.

## ✨ Key Features

### 1. Auto-Login & Data Scraping
- Register once with PRN and DOB
- Automated portal login
- Extract attendance and CIE marks
- Real-time data fetching

### 2. CGPA/SGPA Calculator
- Calculate current semester SGPA
- Track CGPA across semesters
- Target SGPA calculator
- Grade distribution analysis

### 3. Advanced Analytics 🆕
- **Performance Dashboard**: Subject-wise metrics, weak/strong subjects
- **Correlation Analysis**: Attendance vs marks with statistical insights
- **Semester Comparison**: Trend analysis, improvement tracking
- **Grade Predictions**: ESE requirements, achievable grades

### 4. Leaderboards
- Subject-wise rankings
- Exam-type specific leaderboards
- Top performers tracking

## 🏗️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Database (Neon or Prisma)
- **BeautifulSoup4**: Web scraping
- **Uvicorn**: ASGI server

### Database Options
- **Neon PostgreSQL**: Serverless Postgres
- **Prisma Postgres**: Managed Postgres with Accelerate

### ORM
- **Prisma**: TypeScript/JavaScript ORM for Next.js
- **psycopg2**: Python PostgreSQL adapter

## 📂 Project Structure

```
contineo-scraper/
├── api.py                  # FastAPI application
├── analytics.py            # Analytics engine
├── cgpa_calculator.py      # CGPA/SGPA calculations
├── web_scraper.py          # Portal scraping
├── db_utils_neon.py        # Neon database utilities
├── db_utils_prisma.py      # Prisma database utilities
├── config.py               # Configuration
├── prisma/
│   └── schema.prisma       # Database schema
├── docs/                   # Documentation
└── scripts/                # Utility scripts
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies (for Prisma)
npm install
```

### 2. Configure Environment
```bash
# Copy and edit .env file
cp .env.example .env
```

### 3. Setup Database
```bash
# Using Prisma
npx prisma db push
npx prisma generate

# Or using Neon (auto-creates tables on first run)
```

### 4. Run API
```bash
# Development
uvicorn api:app --reload

# Production
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Access API
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 API Endpoints

### User Management
- `POST /api/users/register` - Register new user
- `GET /api/users/{username}` - Get user details

### Data Fetching
- `POST /api/data/fetch/{username}` - Fetch latest data
- `GET /api/data/marks/{username}` - Get stored marks

### CGPA/SGPA
- `GET /api/cgpa/calculate/{username}` - Calculate SGPA
- `POST /api/cgpa/save-semester/{username}` - Save semester
- `GET /api/cgpa/semesters/{username}` - Get all semesters
- `GET /api/cgpa/target/{username}` - Target calculator

### Analytics
- `GET /api/analytics/performance/{username}` - Performance dashboard
- `GET /api/analytics/correlation/{username}` - Attendance correlation
- `GET /api/analytics/semester-comparison/{username}` - Semester trends
- `GET /api/analytics/predictions/{username}` - Grade predictions

### Leaderboards
- `GET /api/leaderboard/{subject}/{exam}` - Get leaderboard

### Configuration
- `GET /api/config/subjects` - Get subject mappings

## 🎨 Next.js Integration

### Install Prisma Client
```bash
npm install @prisma/client
```

### Use in Your App
```typescript
import { prisma } from '@/lib/prisma'

// Get user with all data
const user = await prisma.user.findUnique({
  where: { firstName: 'username' },
  include: {
    cieMarks: true,
    semesters: true
  }
})
```

### Call API
```typescript
const response = await fetch('http://localhost:8000/api/analytics/performance/username')
const data = await response.json()
```

## 📚 Documentation

- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Complete API reference
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Deployment instructions
- **[PRISMA_SETUP.md](./PRISMA_SETUP.md)** - Prisma setup guide
- **[docs/PROJECT_STRUCTURE.md](./docs/PROJECT_STRUCTURE.md)** - Project structure

## 🐳 Deployment

### Docker
```bash
docker-compose up -d
```

### Vercel
```bash
vercel deploy
```

### Railway/Render
Connect your GitHub repo and deploy

## 🔐 Environment Variables

```env
# Neon PostgreSQL
NEON_DB_PASSWORD=your_password
NEON_DB_URI=your_neon_uri
PG_DBNAME=neondb
PG_USER=neondb_owner

# Prisma Postgres
DATABASE_URL=prisma+postgres://...
DIRECT_URL=postgresql://...
```

## 📈 Analytics Features

### 1. Performance Dashboard
```json
{
  "subjects": [...],
  "overall_stats": {
    "average_percentage": 82.5,
    "median_percentage": 85.0,
    "std_deviation": 8.2
  },
  "weak_subjects": [...],
  "strong_subjects": [...]
}
```

### 2. Correlation Analysis
```json
{
  "correlation_coefficient": 0.756,
  "subject_correlations": [...],
  "insights": [
    "Strong positive correlation: Higher attendance leads to better marks"
  ]
}
```

### 3. Semester Comparison
```json
{
  "semester_comparison": [...],
  "trends": {
    "average_sgpa": 8.0,
    "improvement_rate": 0.4
  },
  "trend_direction": "Improving"
}
```

### 4. Grade Predictions
```json
{
  "predictions": [...],
  "recommendations": [
    "Score 9/40 in ESE for O grade"
  ]
}
```

## 🎯 Use Cases

### For Students
- Track attendance and marks
- Calculate CGPA/SGPA
- Plan for target grades
- Compare with peers

### For Developers
- REST API for frontend integration
- Prisma ORM for type-safe queries
- Analytics engine for insights
- Extensible architecture

### For Institutions
- Student performance analytics
- Attendance-marks correlation
- Trend analysis
- Predictive insights

## 🛠️ Development

### Run Tests
```bash
pytest
```

### Format Code
```bash
black .
```

### Type Checking
```bash
mypy .
```

### Prisma Studio
```bash
npx prisma studio
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Support

- **Documentation**: Check the docs/ folder
- **API Docs**: Visit /docs endpoint
- **Issues**: GitHub Issues

## 🎉 What's Next?

1. **Build Next.js Frontend**: Use the API endpoints
2. **Add Authentication**: JWT tokens for security
3. **Implement Caching**: Redis for performance
4. **Add Notifications**: Email alerts for low attendance
5. **Mobile App**: React Native or Flutter

---

**Built with ❤️ for students who want to track their academic progress effortlessly!**
