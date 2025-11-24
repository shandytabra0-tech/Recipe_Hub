# Recipe Hub - Setup Guide

## Prerequisites

Before starting, ensure you have:
1. **Python 3.8+** installed
2. **XAMPP** installed and running
3. **MySQL** service started in XAMPP

## Step-by-Step Setup

### 1. Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

**Note:** If you encounter issues installing `mysqlclient` on Windows, you may need to:
- Install Visual C++ Build Tools
- Or use `pip install mysqlclient` with pre-built wheels
- Alternative: Use `pip install pymysql` and update settings.py to use PyMySQL

### 2. Create MySQL Database

1. Start XAMPP and ensure MySQL service is running
2. Open phpMyAdmin (http://localhost/phpmyadmin)
3. Create a new database named `recipe_hub`
4. Set collation to `utf8mb4_general_ci` (optional but recommended)

### 3. Configure Database Connection

The default settings in `recipe_hub/settings.py` are:
- **Database Name:** `recipe_hub`
- **User:** `root`
- **Password:** (empty - default XAMPP setting)
- **Host:** `localhost`
- **Port:** `3306`

If your MySQL setup is different, edit `recipe_hub/settings.py` and update the `DATABASES` setting.

### 4. Run Database Migrations

Create the database tables by running:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create all necessary tables in your MySQL database.

### 5. Create Admin Superuser

Create an admin account to manage the site:

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 6. Create Sample Categories (Optional)

You can create categories through the admin panel, or use Django shell:

```bash
python manage.py shell
```

Then run:
```python
from recipes.models import Category
Category.objects.create(name="Appetizers", description="Starters and appetizers")
Category.objects.create(name="Main Course", description="Main dishes")
Category.objects.create(name="Desserts", description="Sweet treats")
Category.objects.create(name="Beverages", description="Drinks and beverages")
```

### 7. Start Development Server

Run the Django development server:

```bash
python manage.py runserver
```

### 8. Access the Application

- **Homepage:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## Troubleshooting

### MySQL Connection Issues

If you get MySQL connection errors:

1. **Check MySQL is running** in XAMPP Control Panel
2. **Verify database exists** in phpMyAdmin
3. **Check credentials** in `settings.py`
4. **Try alternative:** Install PyMySQL and update settings:
   ```python
   # At the top of settings.py
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

### Port Already in Use

If port 8000 is busy, use a different port:
```bash
python manage.py runserver 8080
```

### Static Files Not Loading

Run collectstatic (for production):
```bash
python manage.py collectstatic
```

## First Steps After Setup

1. **Login to Admin Panel** with your superuser account
2. **Create Categories** for recipes
3. **Register a test user** on the homepage
4. **Submit a test recipe** as the test user
5. **Approve the recipe** in the admin panel
6. **View the recipe** on the homepage

## Project Structure

```
recipe_hub/
├── manage.py
├── requirements.txt
├── recipe_hub/          # Project settings
│   ├── settings.py      # Database and app configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py
├── recipes/             # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── forms.py         # Form definitions
│   ├── admin.py         # Admin configuration
│   ├── urls.py          # App URL routing
│   └── templates/       # HTML templates
│       └── recipes/
└── media/               # User uploaded files (created automatically)
```

## Features Overview

✅ User registration and authentication
✅ Recipe submission with image uploads
✅ Admin approval workflow
✅ Comments on recipes
✅ Rating system (1-5 stars)
✅ Category filtering
✅ Search functionality
✅ Responsive Bootstrap design
✅ Pagination for recipe lists

## Next Steps

- Customize the design in templates
- Add more features (favorites, recipe collections, etc.)
- Configure for production deployment
- Set up email notifications
- Add recipe editing functionality

