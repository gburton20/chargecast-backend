# Pre-Commit Checklist

Before committing to GitHub and deploying to Render, verify:

## ✅ Files Created/Updated

- [x] `.gitignore` - excludes sensitive files (.env, __pycache__, .venv, etc.)
- [x] `.env.example` - template for environment variables (no secrets)
- [x] `requirements.txt` - clean production dependencies (updated with pip freeze)
- [x] `README.md` - project documentation
- [x] `Procfile` - Render deployment configuration
- [x] `runtime.txt` - Python version specification
- [x] `build.sh` - Build script for Render (executable)
- [x] `DEPLOYMENT.md` - Deployment instructions for Render
- [x] `settings.py` - Updated for production (ALLOWED_HOSTS, STATIC_ROOT, CORS, WhiteNoise)

## ✅ Security Checks

- [x] `.env` file is in `.gitignore` and won't be committed
- [x] No secrets in code (SECRET_KEY uses environment variable)
- [x] CORS configured for production (allows all only in DEBUG mode)
- [x] DEBUG defaults to False
- [x] ALLOWED_HOSTS configured via environment variable

## ✅ Production Configuration

- [x] Gunicorn installed for production server
- [x] WhiteNoise installed for static file serving
- [x] PostgreSQL driver (psycopg2-binary) installed
- [x] Static files configuration (STATIC_ROOT, WhiteNoise middleware)
- [x] Database configuration using environment variables

## 📝 Before First Commit

1. **Review your .env file** - Make sure it contains only development values
2. **Generate a new SECRET_KEY for production** - Don't use the one in your local .env:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```
3. **Test locally** to ensure everything works:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --no-input
   python manage.py runserver
   ```

## 📝 Git Commands to Commit

```bash
# Stage all new and modified files
git add .

# Review what will be committed (make sure .env is NOT listed)
git status

# Commit with a meaningful message
git commit -m "Initial commit: Django backend with carbon intensity API"

# Push to GitHub
git push origin main  # or 'master' depending on your default branch
```

## 📝 After Pushing to GitHub

1. Go to Render dashboard
2. Follow instructions in `DEPLOYMENT.md`
3. Create PostgreSQL database
4. Create Web Service
5. Set environment variables in Render
6. Deploy!

## 🚨 Important Reminders

- **NEVER** commit the `.env` file
- **ALWAYS** generate a new SECRET_KEY for production
- **ALWAYS** set DEBUG=False in production
- **ALWAYS** configure ALLOWED_HOSTS for your domain
- **TEST** your deployment after it's live

## 🔍 Files That Should NOT Be Committed

- `.env` (contains secrets)
- `.venv/` (virtual environment)
- `__pycache__/` (Python cache)
- `db.sqlite3` (local development database)
- `.DS_Store` (macOS system file)

All of these are in `.gitignore` ✓
