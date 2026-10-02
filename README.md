# StudyMate

StudyMate is a simple Django web application that helps students manage subjects, tasks, deadlines, and study progress from one dashboard.

## Features

- Student-friendly dashboard with statistics and progress tracking
- Subject management for each user
- Task management with add, edit, delete, complete, and pending actions
- Search, filtering, and sorting for tasks
- User authentication with registration and login
- Responsive design using Bootstrap 5
- Deployment configuration for Vercel

## Tech Stack

- Python
- Django
- SQLite for local development, with PostgreSQL support when `DATABASE_URL` is set
- Bootstrap 5
- HTML, CSS, and vanilla JavaScript

## Project Structure

```text
studymate/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── build.sh
├── render.yaml
├── README.md
├── studymate/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── planner/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── management/
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── 404.html
│   ├── 500.html
│   ├── registration/
│   └── planner/
├── static/
│   ├── css/
│   └── js/
└── staticfiles/
```

## Installation

### 1. Create a virtual environment

```bash
python -m venv venv
```

This creates an isolated Python environment so your project dependencies do not affect the rest of your system.

### 2. Activate the virtual environment

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs Django and the production deployment dependencies.

### 4. Run migrations

```bash
python manage.py migrate
```

This creates the SQLite database tables required by the project.

### 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

This creates an admin account for the Django admin panel.

### 6. Run the server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Environment Variables

The project uses SQLite locally. For deployment, PostgreSQL is selected automatically when `DATABASE_URL` is set.
Create `.env` only if you need to override local environment settings, and never commit real credentials.

Example:

```env
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app
DATABASE_URL=replace-with-neon-postgresql-url
CSRF_TRUSTED_ORIGINS=https://*.vercel.app
```

You can copy from `.env.example`:

```bash
copy .env.example .env
```

## Using the Application

1. Open the home page.
2. Register a new account.
3. Log in with your account.
4. Add subjects and study tasks.
5. Use the dashboard to track progress.
6. Mark tasks complete when finished.
7. Update your profile from the profile page.

## Admin Panel

To access the admin panel:

```bash
python manage.py createsuperuser
```

Then go to:

```text
http://127.0.0.1:8000/admin/
```

## Sample Data

You can seed sample subjects and tasks:

```bash
python manage.py seed_data
```

## Tests

Run all Django tests with:

```bash
python manage.py test
```

## Deployment on Vercel

Follow the beginner-friendly, step-by-step guide in [DEPLOYMENT.md](DEPLOYMENT.md). Vercel runs Django as a Python function. Add a persistent PostgreSQL database integration such as Neon and set `DATABASE_URL`; SQLite remains the local database.

## GitHub Upload Instructions

Initialize Git if needed:

```bash
git init
git add .
git commit -m "Initial commit for StudyMate"
git branch -M main
git remote add origin <your-repository-url>
git push -u origin main
```

## Common Errors and Solutions

### 1. ImportError or module not found

Run:

```bash
pip install -r requirements.txt
```

### 2. Database migration errors

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Static files not loading in production

Run:

```bash
python manage.py collectstatic
```

### 4. Admin login not working

Make sure you created a superuser using:

```bash
python manage.py createsuperuser
```

## Final Note

This project is designed to be beginner-friendly, clean, and easy to explain during a viva or college project presentation.
