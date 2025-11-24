# Push Recipe Hub to GitHub

## Step 1: Install Git (if not installed)
Download from: https://git-scm.com/download/win

## Step 2: Create GitHub Repository
1. Go to https://github.com
2. Click "New repository"
3. Name: `recipe-hub`
4. Make it public
5. Don't initialize with README (we have files already)
6. Click "Create repository"

## Step 3: Push to GitHub
Open Command Prompt in your project folder and run:

```bash
git init
git add .
git commit -m "Initial commit - Recipe Hub Django app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/recipe-hub.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 4: Deploy to Render
1. Go to https://dashboard.render.com
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will detect `render.yaml` and auto-deploy

Your app will be live at: `https://recipe-hub-XXXX.onrender.com`