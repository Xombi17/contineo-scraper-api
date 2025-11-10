# Frontend Development Context - Contineo Scraper

## 🎯 Project Overview

Build a modern Next.js 14+ web application for a student academic portal that displays attendance, marks, CGPA/SGPA calculations, and advanced analytics. The backend API is already built and running.

---

## 🔗 Backend API Details

### Base URL
```
http://localhost:8000
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Features Available
1. User registration with credential validation
2. Automated data scraping (attendance & CIE marks)
3. CGPA/SGPA calculator with target predictions
4. Advanced analytics (performance dashboard, correlations, predictions)
5. Subject-wise leaderboards

---

## 📊 Core API Endpoints

### Authentication & Users
```typescript
// Register new user (validates with actual portal)
POST /api/users/register
Body: {
  username: string
  full_name: string
  prn: string
  dob_day: string
  dob_month: string
  dob_year: string
}

// Get user details
GET /api/users/{username}
```

### Data Fetching
```typescript
// Fetch latest data from portal
POST /api/data/fetch/{username}
Response: {
  user: { username, full_name, prn }
  attendance: [{ subject: string, percentage: number }]
  cie_marks: { [subject]: { MSE: number, "TH-ISE1": number, ... } }
  scraped_at: string
}

// Get stored marks
GET /api/data/marks/{username}
```

### CGPA/SGPA
```typescript
// Calculate current SGPA
GET /api/cgpa/calculate/{username}
Response: {
  sgpa: number
  total_credits: number
  subjects: [{
    code: string
    name: string
    credits: number
    marks: number
    percentage: number
    grade: string
    grade_point: number
  }]
  grade_distribution: { O: number, A+: number, ... }
}

// Save semester record
POST /api/cgpa/save-semester/{username}
Body: {
  semester_number: number
  semester_name: string
  sgpa: number
  total_credits: number
  academic_year: string
}

// Get all semesters
GET /api/cgpa/semesters/{username}
Response: {
  semester_records: [...]
  cgpa: { cgpa: number, total_credits: number }
}

// Target calculator
GET /api/cgpa/target/{username}?target_sgpa=8.5
Response: {
  is_achievable: boolean
  current_sgpa: number
  target_sgpa: number
  recommendations: [{
    subject: string
    minimum_marks_needed: number
    grade_needed: string
  }]
}
```

### Analytics (Advanced Features)
```typescript
// Performance Dashboard
GET /api/analytics/performance/{username}
Response: {
  subjects: [{ code, name, type, percentage, grade, completion_rate }]
  overall_stats: { average_percentage, median, std_deviation }
  weak_subjects: [...]
  strong_subjects: [...]
}

// Attendance-Marks Correlation
GET /api/analytics/correlation/{username}
Response: {
  correlation_coefficient: number
  subject_correlations: [{ subject, attendance, marks_percentage, difference }]
  insights: string[]
  interpretation: string
}

// Semester Comparison
GET /api/analytics/semester-comparison/{username}
Response: {
  semester_comparison: [{ semester_number, sgpa, credits }]
  trends: { average_sgpa, highest, lowest, consistency }
  best_semester: { semester_number, sgpa }
  improvement_rate: number
  trend_direction: "Improving" | "Declining" | "Stable"
}

// Grade Predictions
GET /api/analytics/predictions/{username}
Response: {
  predictions: [{
    subject: string
    current_marks: number
    ese_pending: boolean
    grade_predictions: { O: { ese_marks_needed, achievable }, ... }
  }]
  recommendations: string[]
}
```

### Leaderboards
```typescript
// Get subject leaderboard
GET /api/leaderboard/{subject_code}/{exam_type}?limit=10
Response: {
  subject_code: string
  exam_type: string
  leaderboard: [{ rank: number, name: string, marks: number }]
}
```

---

## 🎨 Design Requirements

### Color Scheme
- **Primary**: Purple/Blue gradient (#667eea to #764ba2)
- **Success**: Green (#28a745)
- **Warning**: Yellow (#ffc107)
- **Danger**: Red (#dc3545)
- **Background**: Light gray (#f8f9fa)

### Typography
- **Headings**: Bold, modern sans-serif
- **Body**: Clean, readable font
- **Monospace**: For PRN, codes

### UI Components Needed

#### 1. Authentication
- **Login/Register Page**
  - Username input
  - Full name, PRN, DOB fields
  - Credential validation with loading state
  - Error handling

#### 2. Dashboard (Main Page)
- **Header**
  - User name and PRN
  - Last updated timestamp
  - Refresh button
  - Logout button

- **Quick Stats Cards**
  - Average Attendance (with color coding)
  - Current SGPA
  - Credits Earned
  - Total Subjects

- **Attendance Section**
  - Bar chart showing attendance per subject
  - Color coding: Green (≥85%), Yellow (75-84%), Red (<75%)
  - Red line at 75% minimum
  - Expandable cards per subject with predictor

- **Marks Section**
  - Subject cards with marks breakdown
  - Grade badges (O, A+, A, B+, etc.)
  - Progress bars for completion
  - Expandable for detailed view

#### 3. CGPA Calculator Page
- **Current SGPA Tab**
  - SGPA metric card
  - Grade distribution pie chart
  - Subject-wise table with grades
  - Save semester button

- **CGPA Tracker Tab**
  - Overall CGPA metric
  - Semester-wise table
  - Line chart showing SGPA trend
  - Best semester highlight

- **Target Calculator Tab**
  - Target SGPA input slider
  - Calculate button
  - Recommendations cards per subject
  - Achievability indicator

#### 4. Analytics Page
- **Performance Dashboard**
  - Radar chart for subject comparison
  - Overall statistics cards
  - Weak/strong subjects lists
  - Subject type breakdown

- **Correlation Analysis**
  - Scatter plot: Attendance vs Marks
  - Correlation coefficient display
  - Insights cards
  - Subject-wise comparison table

- **Semester Trends**
  - Line chart: SGPA over semesters
  - Trend direction indicator
  - Improvement rate metric
  - Best/worst semester cards

- **Predictions**
  - Subject cards with ESE requirements
  - Grade target badges
  - Achievability indicators
  - Action items list

#### 5. Leaderboards Page
- **Subject Selector**
  - Dropdown for subject
  - Dropdown for exam type
  - Refresh button

- **Leaderboard Table**
  - Rank, Name, Marks columns
  - Medal icons for top 3
  - Highlight current user
  - Animated transitions

---

## 🛠️ Tech Stack Recommendations

### Core
- **Next.js 14+** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **shadcn/ui** for components

### Data Fetching
- **SWR** or **TanStack Query** for API calls
- **Axios** for HTTP client

### Charts & Visualizations
- **Recharts** or **Chart.js** for charts
- **Framer Motion** for animations

### State Management
- **Zustand** or **Context API** for global state
- **Local Storage** for username persistence

### Forms
- **React Hook Form** for form handling
- **Zod** for validation

---

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 640px (single column)
- **Tablet**: 640px - 1024px (2 columns)
- **Desktop**: > 1024px (3-4 columns)

### Mobile-First Features
- Hamburger menu
- Swipeable cards
- Bottom navigation
- Pull-to-refresh

---

## 🎯 User Flows

### First-Time User
1. Land on login page
2. Click "Register"
3. Fill in credentials
4. System validates with portal
5. Redirect to dashboard
6. Show onboarding tour

### Returning User
1. Enter username (auto-filled from localStorage)
2. Click "Login"
3. Redirect to dashboard
4. Show last updated time
5. Option to refresh data

### Data Refresh
1. Click refresh button
2. Show loading spinner
3. Fetch from portal (takes 5-10 seconds)
4. Update all sections
5. Show success toast

---

## 🔐 Security Considerations

- Store only username in localStorage (no passwords)
- Use HTTPS in production
- Implement rate limiting on frontend
- Show loading states during API calls
- Handle errors gracefully
- Validate all inputs

---

## 📊 Data Visualization Examples

### Attendance Bar Chart
```typescript
{
  subjects: ["SPCC", "CSS", "MC", "AI"],
  percentages: [85, 72, 91, 78],
  colors: ["green", "red", "green", "yellow"]
}
```

### SGPA Trend Line Chart
```typescript
{
  semesters: [1, 2, 3, 4, 5, 6, 7],
  sgpa: [7.2, 7.5, 7.8, 8.0, 8.2, 8.1, 8.5]
}
```

### Performance Radar Chart
```typescript
{
  subjects: ["SPCC", "CSS", "MC", "AI", "Lab1", "Lab2"],
  percentages: [88, 75, 92, 80, 95, 90]
}
```

---

## 🎨 Component Examples

### Attendance Card
```tsx
<Card>
  <CardHeader>
    <h3>SPCC (System Programming)</h3>
    <Badge color={percentage >= 85 ? "green" : percentage >= 75 ? "yellow" : "red"}>
      {percentage}%
    </Badge>
  </CardHeader>
  <CardContent>
    <ProgressBar value={percentage} max={100} />
    <Button onClick={showPredictor}>Attendance Predictor</Button>
  </CardContent>
</Card>
```

### SGPA Metric
```tsx
<MetricCard>
  <MetricValue>{sgpa.toFixed(2)}</MetricValue>
  <MetricLabel>Current SGPA</MetricLabel>
  <MetricDelta positive={sgpa >= 7.5}>
    {sgpa >= 7.5 ? "Good Standing" : "Needs Improvement"}
  </MetricDelta>
</MetricCard>
```

### Subject Performance Card
```tsx
<SubjectCard>
  <SubjectHeader>
    <SubjectName>SPCC</SubjectName>
    <GradeBadge grade="A+">{gradePoint}/10</GradeBadge>
  </SubjectHeader>
  <MarksBreakdown>
    <Mark label="MSE" value={18} max={20} />
    <Mark label="ISE1" value={45} max={50} />
    <Mark label="ISE2" value={18} max={20} />
    <Mark label="ESE" value={35} max={40} />
  </MarksBreakdown>
  <TotalMarks>{total}/100 ({percentage}%)</TotalMarks>
</SubjectCard>
```

---

## 🚀 Performance Optimization

- Use **Next.js Image** for optimized images
- Implement **lazy loading** for charts
- Use **React.memo** for expensive components
- Implement **virtual scrolling** for long lists
- Cache API responses with SWR
- Use **Suspense** for loading states

---

## 🧪 Testing Considerations

- Test with different screen sizes
- Test with slow network (loading states)
- Test error scenarios (API failures)
- Test with empty data
- Test with maximum data
- Test accessibility (keyboard navigation, screen readers)

---

## 📝 Sample API Call (TypeScript)

```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function fetchStudentData(username: string) {
  const response = await fetch(`${API_BASE}/api/data/fetch/${username}`, {
    method: 'POST',
  })
  
  if (!response.ok) {
    throw new Error('Failed to fetch data')
  }
  
  return response.json()
}

export async function getPerformanceAnalytics(username: string) {
  const response = await fetch(`${API_BASE}/api/analytics/performance/${username}`)
  return response.json()
}

// Usage in component
'use client'
import useSWR from 'swr'

export default function Dashboard({ username }: { username: string }) {
  const { data, error, isLoading } = useSWR(
    `/analytics/performance/${username}`,
    () => getPerformanceAnalytics(username)
  )

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage />

  return <PerformanceDashboard data={data} />
}
```

---

## 🎯 Key Features to Highlight

1. **Real-time Data**: Fetches live data from student portal
2. **Smart Analytics**: AI-powered insights and predictions
3. **Beautiful Visualizations**: Interactive charts and graphs
4. **Target Planning**: Calculate what you need for desired SGPA
5. **Leaderboards**: Compare with peers
6. **Responsive Design**: Works on all devices
7. **Fast & Cached**: Smart caching for instant load times

---

## 📦 Deliverables

### Pages
1. `/` - Login/Register
2. `/dashboard` - Main dashboard
3. `/cgpa` - CGPA calculator
4. `/analytics` - Advanced analytics
5. `/leaderboard` - Subject leaderboards
6. `/profile` - User settings

### Components
- Layout (Header, Sidebar, Footer)
- Auth forms (Login, Register)
- Metric cards
- Charts (Bar, Line, Radar, Pie)
- Data tables
- Loading states
- Error boundaries
- Toast notifications

---

## 🎨 Design Inspiration

- **Modern**: Clean, minimal, lots of white space
- **Colorful**: Use gradients and vibrant colors
- **Interactive**: Smooth animations and transitions
- **Data-Driven**: Focus on visualizations
- **Mobile-First**: Touch-friendly, swipeable

### Similar Apps for Reference
- Notion (clean UI)
- Linear (smooth animations)
- Vercel Dashboard (metrics display)
- GitHub (data tables)
- Stripe Dashboard (charts)

---

## ⚡ Quick Start Command

```bash
# Create Next.js app
npx create-next-app@latest contineo-frontend --typescript --tailwind --app

# Install dependencies
npm install swr axios recharts framer-motion zustand
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu
npm install lucide-react class-variance-authority clsx tailwind-merge

# Install shadcn/ui
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card input label badge
```

---

## 🎯 Success Criteria

- ✅ Clean, modern UI matching design system
- ✅ All API endpoints integrated
- ✅ Responsive on mobile, tablet, desktop
- ✅ Fast load times (< 2s)
- ✅ Smooth animations
- ✅ Error handling
- ✅ Loading states
- ✅ Accessible (WCAG 2.1 AA)

---

**Use this context to build a beautiful, functional Next.js frontend that students will love! 🚀**
