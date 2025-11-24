# Recipe Hub

A comprehensive Django-based recipe sharing platform where users can submit recipes, rate and comment on them, with admin approval workflow.

## Features

- User registration and authentication
- Recipe submission with image uploads
- Admin approval system for recipes
- Comments and ratings on recipes
- Category-based filtering
- Search functionality
- Responsive design

## Quick Start

### Option 1: Automated Setup (Windows)

1. **Start MySQL in XAMPP**
2. **Create database `recipe_hub` in phpMyAdmin**
3. **Run the setup script:**
   ```bash
   setup.bat
   ```
4. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```
5. **Start server:**
   ```bash
   python manage.py runserver
   ```

### Option 2: Manual Setup

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed step-by-step instructions.

### Prerequisites

1. Python 3.8 or higher
2. XAMPP (for MySQL)
3. pip (Python package manager)

### Quick Installation Steps

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start MySQL service in XAMPP**

3. **Create MySQL database:**
   - Open phpMyAdmin (http://localhost/phpmyadmin)
   - Create a new database named `recipe_hub`

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Homepage: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
recipe_hub/
├── manage.py
├── requirements.txt
├── recipe_hub/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── recipes/             # Main app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
└── media/               # User uploaded files
```

## User Roles

- **Regular Users**: Can register, submit recipes, comment, and rate
- **Admin**: Can approve/reject recipes, manage all content

## Development Phases

This project follows a 12-phase development approach covering planning, database design, admin setup, core functionality, frontend, user features, interactive features, admin controls, media handling, testing, security, and deployment preparation.

