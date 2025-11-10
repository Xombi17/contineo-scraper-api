# Student Portal Frontend

Beautiful, modern Next.js frontend for the Contineo Scraper API.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 🌐 Access

- **Development**: http://localhost:3000
- **API Backend**: http://localhost:8000

## ✨ Features

- 🎨 Modern, responsive UI with Tailwind CSS
- 📊 Interactive charts with Recharts
- 🔄 Real-time data fetching with SWR
- 📱 Mobile-first design
- 🎯 Beautiful gradients and animations
- 📈 Attendance tracking with color coding
- 🏆 Grade distribution visualization
- 📝 Subject-wise performance cards

## 📦 Tech Stack

- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **SWR** - Data fetching
- **Recharts** - Charts
- **Lucide React** - Icons

## 🎨 Pages

- `/` - Login/Register
- `/dashboard` - Main dashboard with attendance, marks, and SGPA

## 🔧 Configuration

Edit `.env.local` to change API URL:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📱 Responsive Design

- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

## 🎯 Features Implemented

✅ User authentication (login/register)
✅ Dashboard with key metrics
✅ Attendance bar chart with color coding
✅ Subject performance cards
✅ Grade distribution
✅ SGPA calculation
✅ Responsive design
✅ Loading states
✅ Error handling
✅ Data refresh

## 🚀 Deployment

### Vercel (Recommended)
```bash
vercel deploy
```

### Docker
```bash
docker build -t student-portal-frontend .
docker run -p 3000:3000 student-portal-frontend
```

## 📝 Notes

- Make sure the backend API is running at http://localhost:8000
- Username is stored in localStorage
- Data is cached with SWR for better performance

---

**Built with ❤️ for students**
