@echo off
echo ====================================
echo Recipe Hub - Setup Script
echo ====================================
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Creating database migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo ERROR: Failed to create migrations
    pause
    exit /b 1
)

echo.
echo Step 3: Applying database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to apply migrations
    echo Make sure MySQL is running in XAMPP and database 'recipe_hub' exists
    pause
    exit /b 1
)

echo.
echo Step 4: Creating media directory...
if not exist "media" mkdir media
if not exist "media\recipe_images" mkdir media\recipe_images

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Create a superuser: python manage.py createsuperuser
echo 2. Start the server: python manage.py runserver
echo 3. Open http://127.0.0.1:8000 in your browser
echo.
pause

