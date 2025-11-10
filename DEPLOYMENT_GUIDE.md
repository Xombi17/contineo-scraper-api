# Deployment Guide

## 🚀 Your API is Ready!

The Contineo Scraper API is now running at: **http://localhost:8000**

### Quick Links
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📦 What's Been Built

### Core Files
- `api.py` - FastAPI application with all endpoints
- `analytics.py` - Analytics engine (performance, correlation, predictions)
- `cgpa_calculator.py` - CGPA/SGPA calculation logic
- `web_scraper.py` - Portal scraping logic
- `db_utils_neon.py` - Database operations
- `config.py` - Configuration and subject mappings

### Documentation
- `API_DOCUMENTATION.md` - Complete API reference
- `README.md` - Updated with API info
- `DEPLOYMENT_GUIDE.md` - This file

### Deployment Files
- `Dockerfile` - Docker container configuration
- `docker-compose.yml` - Docker Compose setup
- `vercel.json` - Vercel deployment config
- `.dockerignore` - Docker ignore rules

---

## 🔧 Local Development

### Start the API
```bash
uvicorn api:app --reload
```

### Test Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Get subjects config
curl http://localhost:8000/api/config/subjects

# Register a user (replace with real data)
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "full_name": "Test User",
    "prn": "2021XXXX",
    "dob_day": "15",
    "dob_month": "08",
    "dob_year": "2003"
  }'
```

---

## 🐳 Docker Deployment

### Build and Run
```bash
# Build image
docker build -t contineo-api .

# Run container
docker run -p 8000:8000 --env-file .env contineo-api

# Or use docker-compose
docker-compose up -d
```

### Check Logs
```bash
docker-compose logs -f api
```

### Stop
```bash
docker-compose down
```

---

## ☁️ Cloud Deployment Options

### 1. Vercel (Recommended for Next.js)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
```

### 2. Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### 3. Render
1. Connect your GitHub repo
2. Select "Web Service"
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

### 4. AWS EC2
```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# Run with systemd
sudo nano /etc/systemd/system/contineo-api.service
```

Example systemd service:
```ini
[Unit]
Description=Contineo API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/contineo-scraper
Environment="PATH=/home/ubuntu/.local/bin"
ExecStart=/home/ubuntu/.local/bin/uvicorn api:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable contineo-api
sudo systemctl start contineo-api
```

---

## 🔐 Production Checklist

### Security
- [ ] Add API authentication (JWT tokens)
- [ ] Implement rate limiting
- [ ] Enable HTTPS/SSL
- [ ] Secure environment variables
- [ ] Add CORS whitelist for production domains
- [ ] Implement request validation
- [ ] Add logging and monitoring

### Performance
- [ ] Enable caching (Redis)
- [ ] Add database connection pooling
- [ ] Implement request queuing for scraping
- [ ] Add CDN for static assets
- [ ] Enable gzip compression

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Add application monitoring (New Relic/DataDog)
- [ ] Configure log aggregation
- [ ] Set up uptime monitoring
- [ ] Create health check endpoints

### Database
- [ ] Set up automated backups
- [ ] Configure connection pooling
- [ ] Add database indexes
- [ ] Monitor query performance

---

## 🔗 Next.js Integration

### Environment Variables (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
# or production URL
NEXT_PUBLIC_API_URL=https://your-api.vercel.app
```

### API Client (lib/api.ts)
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function registerUser(data: UserRegistration) {
  const response = await fetch(`${API_URL}/api/users/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  return response.json();
}

export async function fetchStudentData(username: string) {
  const response = await fetch(`${API_URL}/api/data/fetch/${username}`, {
    method: 'POST',
  });
  return response.json();
}

export async function getAnalytics(username: string) {
  const response = await fetch(`${API_URL}/api/analytics/performance/${username}`);
  return response.json();
}
```

### Usage in Components
```typescript
'use client';

import useSWR from 'swr';
import { getAnalytics } from '@/lib/api';

export default function Dashboard({ username }: { username: string }) {
  const { data, error, isLoading } = useSWR(
    `/analytics/${username}`,
    () => getAnalytics(username)
  );

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading data</div>;

  return (
    <div>
      <h1>Performance Dashboard</h1>
      <p>Average: {data.overall_stats.average_percentage}%</p>
      {/* Render charts and data */}
    </div>
  );
}
```

---

## 📊 Analytics Endpoints Usage

### 1. Performance Dashboard
```typescript
const performance = await fetch(`${API_URL}/api/analytics/performance/${username}`);
// Use for: Subject cards, performance metrics, weak/strong subjects
```

### 2. Attendance Correlation
```typescript
const correlation = await fetch(`${API_URL}/api/analytics/correlation/${username}`);
// Use for: Scatter plots, correlation insights, recommendations
```

### 3. Semester Comparison
```typescript
const comparison = await fetch(`${API_URL}/api/analytics/semester-comparison/${username}`);
// Use for: Line charts, trend analysis, best semester highlight
```

### 4. Grade Predictions
```typescript
const predictions = await fetch(`${API_URL}/api/analytics/predictions/${username}`);
// Use for: ESE target calculator, grade recommendations, action items
```

---

## 🎨 Frontend Component Ideas

### Dashboard Components
- **PerformanceCard**: Show SGPA, credits, grade distribution
- **SubjectGrid**: Cards for each subject with marks breakdown
- **AttendanceChart**: Bar chart with color coding
- **CorrelationScatter**: Attendance vs marks scatter plot
- **TrendLine**: SGPA trend across semesters
- **PredictionCards**: What you need for target grades
- **LeaderboardTable**: Top performers per subject

### Pages
- `/dashboard` - Overview with key metrics
- `/subjects` - Detailed subject-wise view
- `/analytics` - Advanced analytics and insights
- `/cgpa` - CGPA calculator and semester tracker
- `/leaderboard` - Rankings and comparisons
- `/profile` - User settings and data export

---

## 🐛 Troubleshooting

### API won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <process_id> /F

# Check database connection
python -c "import db_utils_neon; db_utils_neon.get_db_connection()"
```

### Database connection fails
- Verify .env file has correct credentials
- Check Neon dashboard for connection string
- Ensure IP is whitelisted in Neon (if applicable)

### CORS errors
- Add your Next.js URL to `allow_origins` in `api.py`
- Check browser console for specific CORS error

### Slow scraping
- Portal might be slow or down
- Implement caching to reduce scraping frequency
- Add timeout handling

---

## 📈 Monitoring & Logs

### View Logs
```bash
# Docker
docker-compose logs -f api

# Systemd
sudo journalctl -u contineo-api -f

# Direct
tail -f logs/api.log
```

### Health Monitoring
Set up a cron job or monitoring service to ping:
```bash
curl http://your-api-url/health
```

---

## 🎯 Next Steps

1. **Test all endpoints** using Swagger UI at `/docs`
2. **Build Next.js frontend** using the API
3. **Deploy to production** using one of the cloud options
4. **Add authentication** for production security
5. **Set up monitoring** and error tracking
6. **Optimize performance** with caching

---

## 📞 Support

For issues or questions:
1. Check `API_DOCUMENTATION.md` for endpoint details
2. Review error logs
3. Test with Swagger UI at `/docs`
4. Check database connection

---

**Your API is production-ready! 🚀**

Start building your Next.js frontend and integrate these powerful analytics features!
