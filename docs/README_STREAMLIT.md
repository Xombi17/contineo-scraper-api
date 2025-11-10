# 🎓 Student Portal - Streamlit App

A modern, beautiful web application for viewing student attendance, marks, and calculating CGPA/SGPA.

## ✨ Features

- 📊 **Dashboard** - Overview of attendance and performance
- 📝 **Marks & Leaderboard** - View CIE marks and subject rankings
- 🎯 **CGPA Calculator** - Calculate current SGPA, track CGPA, and plan target grades
- 📈 **Analytics** - Visual insights into performance trends

## 🚀 Quick Start (Streamlit Cloud)

### 1. Deploy to Streamlit Cloud

1. Fork/clone this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository
5. Set main file: `src/st_main.py`
6. Click "Deploy"

### 2. Add Database Secrets

In your Streamlit Cloud app settings:

1. Go to Settings → Secrets
2. Add your database URL:

```toml
DIRECT_URL = "postgresql://user:password@host:port/database?sslmode=require"
```

**Get your database URL:**
- **Prisma Postgres**: Dashboard → Settings → Connection strings → Direct URL
- **Neon**: Console → Connection Details → Connection string

### 3. Done! 🎉

Your app will automatically redeploy with the database connected.

## 💻 Local Development

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo 'DIRECT_URL="your_database_url"' > .env

# Run setup check
python setup_streamlit.py

# Start the app
streamlit run src/st_main.py
```

### Configuration

Create `.streamlit/secrets.toml` for local development:

```toml
DIRECT_URL = "postgresql://user:password@host:port/database"
```

**Important:** Never commit `secrets.toml` to Git!

## 📊 Database Setup

The app automatically creates required tables on first run:
- `users` - Student information
- `cie_marks` - Exam marks and leaderboard data
- `semester_records` - SGPA/CGPA tracking

## 🎨 Features Overview

### Dashboard Tab
- Quick stats (SGPA, Credits, Attendance)
- Color-coded attendance cards
- Interactive attendance chart

### Marks & Leaderboard Tab
- Subject-wise marks breakdown
- Top performers leaderboard
- Medal rankings (🥇🥈🥉)

### CGPA Calculator Tab
- **Current SGPA**: View this semester's performance
- **CGPA Tracker**: Track cumulative GPA across semesters
- **Target Calculator**: Calculate marks needed for target SGPA

### Analytics Tab
- Marks vs Attendance comparison
- Grade point radar chart
- Performance insights

## 🔧 Troubleshooting

### Database Connection Error

```
Error connecting to database
```

**Solution:**
1. Verify your `DIRECT_URL` is correct
2. Ensure it includes `?sslmode=require` for cloud databases
3. Check database is accessible from Streamlit Cloud

### Import Errors

```
ModuleNotFoundError: No module named 'plotly'
```

**Solution:**
1. Ensure `requirements.txt` is in repository root
2. Redeploy the app from Streamlit Cloud

### Secrets Not Loading

**Solution:**
1. Check TOML format in secrets (no quotes around keys)
2. Restart app from Streamlit Cloud dashboard
3. Wait a few seconds for secrets to propagate

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DIRECT_URL` | PostgreSQL connection string | Yes |
| `DATABASE_URL` | Alternative Neon database URL | No |

## 🔒 Security

- Never commit `.env` or `secrets.toml` to Git
- Use different databases for development and production
- Rotate database credentials regularly

## 📚 Documentation

- [Full Deployment Guide](STREAMLIT_DEPLOYMENT.md)
- [Database Schema](STREAMLIT_DEPLOYMENT.md#-database-setup)
- [Customization](STREAMLIT_DEPLOYMENT.md#-customization)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📄 License

MIT License - feel free to use for your own projects!

## 🆘 Support

Having issues? Check:
1. [Deployment Guide](STREAMLIT_DEPLOYMENT.md)
2. Streamlit Cloud logs
3. Database connection settings

---

Made with ❤️ using Streamlit
