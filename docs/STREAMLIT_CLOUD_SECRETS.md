# 🔐 Add Secrets to Streamlit Cloud

## Step-by-Step Guide

### 1. Go to Your App Settings

1. Visit your Streamlit Cloud app: https://better-contineo.streamlit.app
2. Click the **hamburger menu** (☰) in the top right
3. Click **Settings**

### 2. Add Secrets

1. In the Settings page, find the **Secrets** section
2. Click on **Secrets** in the left sidebar
3. You'll see a text editor

### 3. Paste This Configuration

Copy and paste this EXACTLY into the secrets editor:

```toml
DIRECT_URL = "postgresql://3542a5d5336131d834b2f745afe9daa02623c6e69a97f86e1b2a9fc3084dab54:sk_zY_1LaKHDlI8boNayH6N2@db.prisma.io:5432/postgres?sslmode=require"
```

### 4. Save

1. Click **Save** button
2. Your app will automatically restart
3. Wait 30-60 seconds for the app to redeploy

### 5. Verify

1. Go back to your app
2. Enter a username (e.g., "deon" or "anushka")
3. Click "Fetch Data"
4. Data should load from your database!

## ⚠️ Important Security Notes

**Your database credentials are now public in this chat!** 

To secure your database:

1. **Rotate your Prisma credentials:**
   - Go to Prisma Console: https://console.prisma.io
   - Navigate to your project
   - Go to Settings → Connection strings
   - Click "Rotate credentials" or "Generate new password"
   - Update the new URL in Streamlit Cloud secrets

2. **Never commit secrets to Git:**
   - `.streamlit/secrets.toml` is already in `.gitignore`
   - Never share database URLs publicly

3. **Use different credentials for production:**
   - Consider creating a separate database user with limited permissions
   - Use read-only access if the app only needs to read data

## 🔧 Troubleshooting

### App Still Not Working?

1. **Check the logs:**
   - Click hamburger menu → Manage app → Logs
   - Look for database connection errors

2. **Verify secrets format:**
   - Make sure there are no extra spaces
   - Make sure the URL is on one line
   - Make sure you used `DIRECT_URL` (not `DATABASE_URL`)

3. **Test locally first:**
   ```bash
   streamlit run src/st_main.py
   ```

### Common Errors

**"Error connecting to database"**
- Check that DIRECT_URL is set correctly
- Verify the URL includes `?sslmode=require`

**"Module not found"**
- Make sure requirements.txt is properly formatted
- Check that all dependencies are listed

## ✅ Success!

Once secrets are added, your app should:
- Connect to the Prisma Postgres database
- Load user data when you enter a username
- Display attendance, marks, and CGPA calculations
- Show leaderboards and analytics

---

**Need help?** Check the app logs in Streamlit Cloud dashboard.
