# Recipe Hub - Render Deployment Guide

## Prerequisites
- GitHub account
- Render account (free tier available)

## Deployment Steps

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Deploy on Render

#### Option A: Using render.yaml (Recommended)
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and create:
   - Web service for the Django app
   - PostgreSQL database

#### Option B: Manual Setup
1. **Create Database:**
   - Click "New" → "PostgreSQL"
   - Name: `recipe-hub-db`
   - Plan: Free
   - Note the database URL

2. **Create Web Service:**
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Settings:
     - Name: `recipe-hub`
     - Environment: `Python 3`
     - Build Command: `./build.sh`
     - Start Command: `gunicorn recipe_hub.wsgi:application`

3. **Environment Variables:**
   - `SECRET_KEY`: Generate a secure key
   - `DEBUG`: `false`
   - `DATABASE_URL`: (Auto-filled if using Render PostgreSQL)

### 3. Post-Deployment
1. **Create Superuser:**
   - Go to Render dashboard → Your service → Shell
   - Run: `python manage.py createsuperuser`

2. **Access Your App:**
   - Your app will be available at: `https://your-app-name.onrender.com`
   - Admin panel: `https://your-app-name.onrender.com/admin/`

## Important Notes

### Media Files
- Render's ephemeral filesystem means uploaded images won't persist
- For production, consider using:
  - AWS S3
  - Cloudinary
  - Render's persistent disk (paid feature)

### Database
- Free PostgreSQL database sleeps after 90 days of inactivity
- Upgrade to paid plan for production use

### Performance
- Free tier services sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Upgrade to paid plan for always-on service

## Troubleshooting

### Build Failures
- Check build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify `build.sh` has correct permissions

### Database Issues
- Ensure `DATABASE_URL` environment variable is set
- Check database connection in Render logs

### Static Files
- WhiteNoise handles static files automatically
- Run `python manage.py collectstatic` if needed

## Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```