# Host StudyMate on Vercel

This deploys the existing Django project to a public Vercel HTTPS URL. The website, existing Django routes, and UI are unchanged. Vercel runs Django as a Python serverless function.

## 1. Test locally

In PowerShell:

```powershell
cd C:\Users\kavya\OneDrive\Desktop\project\studymate
pip install -r requirements.txt
python manage.py makemigrations --check
python manage.py migrate
python manage.py check
python manage.py test
python manage.py collectstatic --no-input
python manage.py runserver
```

Confirm the site works at `http://127.0.0.1:8000/`.

## 2. Create a private GitHub repository

On GitHub, create an empty repository named `studymate` and choose **Private**. Do not initialize it with a README or other files.

## 3. Push the existing project

In PowerShell, from the project directory:

```powershell
git init
git add .
git commit -m "Prepare StudyMate for deployment"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/studymate.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Git Credential Manager will prompt for GitHub browser authentication if needed; never paste a password or token into project files.

The `.gitignore` prevents `.env`, SQLite database files, virtual environments, Python bytecode, and generated `staticfiles` from being pushed.

## 4. Create a Vercel account and connect GitHub

Sign in to [vercel.com](https://vercel.com) using GitHub and approve access to the private repository.

## 5. Import StudyMate

In Vercel, select **Add New → Project**, import the `studymate` repository, and keep the project root as the repository root. Vercel detects the Python function in `api/index.py` and installs the packages from `requirements.txt`.

## 6. Configure the build and function

The repository's `vercel.json` already contains the build command and routes. If the dashboard asks for these values, use:

Build command:

```bash
python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

The Python entry point is `api/index.py`, which loads the existing Django WSGI application. Vercel routes web requests to this function. WhiteNoise serves collected static files bundled with the function.

## 7. Set environment variables

Add these in **Project → Settings → Environment Variables**:

- `SECRET_KEY`: a new, long random value; do not reuse or publish it.
- `DEBUG`: `False`.
- `DATABASE_URL`: connection string from the PostgreSQL integration described below.
- `ALLOWED_HOSTS`: `.vercel.app` (and add any custom domain host if you use one).
- `CSRF_TRUSTED_ORIGINS`: `https://*.vercel.app` (and add `https://your-custom-domain` if used).

Vercel provides `VERCEL_URL` and `VERCEL_PROJECT_PRODUCTION_URL`; Django adds those hostnames to its allowed hosts and HTTPS CSRF origins.

## 8. Connect a persistent database

Vercel serverless storage is not a persistent place for SQLite. A local SQLite file can be lost, so use PostgreSQL for hosted data:

1. In Vercel Marketplace, add a PostgreSQL provider such as Neon to the project.
2. Create the database using the provider's free option if currently available.
3. Add its pooled or direct connection string as `DATABASE_URL` in Vercel.
4. Redeploy so the build command applies Django migrations to PostgreSQL.

The current `settings.py` keeps SQLite when `DATABASE_URL` is absent and uses PostgreSQL when it is present. Check the provider's current free-tier limits and storage policy before relying on it for long-term data.

## 9. Deploy and open your URL

Select **Deploy**. When the build completes, open the HTTPS URL shown by Vercel. Subsequent pushes to the connected branch trigger redeployments.

## 10. Create hosted admin login

Local SQLite users and passwords are not copied into hosted PostgreSQL. Create an admin user after deployment using Vercel's supported project command/terminal workflow, or temporarily run the one-time management command as part of a secure deployment workflow:

```bash
python manage.py createsuperuser
```

Do not add a fixed username or password to source code or a committed build script. Then verify `/admin/` using the new credentials.

## 11. Test the public site

Check the public HTTPS URL and test:

1. Home page and CSS/JavaScript.
2. Registration, login, and logout.
3. Dashboard.
4. Add/edit/delete subjects.
5. Add/edit/delete tasks, search, filters, sorting, and completion toggles.
6. Profile update.
7. Admin at `/admin/`.

Vercel deployments and functions can have plan-dependent runtime limits. If you encounter a function timeout or unsupported runtime limitation, use a Django-oriented host such as Render instead.
