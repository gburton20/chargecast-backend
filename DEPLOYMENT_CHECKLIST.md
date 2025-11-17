# Deployment Checklist - Render & Railway

## ✅ Pre-Deployment Checklist

Before deploying to Render or Railway, verify all items below:

### 1. Configuration Files

- [x] **Procfile** - Uncommented and properly configured
- [x] **runtime.txt** - Uses `python-3.12` (not `python-3.12.0`)
- [x] **requirements.txt** - Contains all dependencies including:
  - [x] `gunicorn`
  - [x] `dj-database-url`
  - [x] `psycopg2-binary`
  - [x] `whitenoise`
  - [x] `django-cors-headers`
- [x] **build.sh** - Executable permissions (`chmod +x build.sh`)
- [x] **start.sh** - Executable permissions (`chmod +x start.sh`)

### 2. Django Settings (settings.py)

- [x] **DEBUG** - Set to `False` in production (via environment variable)
- [x] **SECRET_KEY** - Read from environment variable
- [x] **ALLOWED_HOSTS** - Includes `.railway.app` and `.onrender.com`
- [x] **CSRF_TRUSTED_ORIGINS** - Set for Railway and Render domains
- [x] **DATABASE_URL** - Configured with `dj-database-url`
- [x] **STATIC_ROOT** - Set to `staticfiles/`
- [x] **STATIC_URL** - Set to `static/`
- [x] **WhiteNoise** - In MIDDLEWARE and STORAGES
- [x] **CORS** - Configured with `django-cors-headers`

### 3. Database Configuration

- [x] **dj-database-url** - Installed and configured
- [x] **psycopg2-binary** - In requirements.txt
- [x] **Fallback config** - Individual DB env vars for local development
- [x] **Connection pooling** - `conn_max_age=600`
- [x] **Health checks** - `conn_health_checks=True`

### 4. Static Files

- [x] **WhiteNoise** - Installed and in MIDDLEWARE
- [x] **STATIC_ROOT** - Configured
- [x] **collectstatic** - In build script
- [x] **CompressedManifestStaticFilesStorage** - Configured

### 5. Environment Variables (.env.example updated)

Required variables documented:
- [x] `DEBUG=False`
- [x] `SECRET_KEY=<generate-secure-key>`
- [x] `ALLOWED_HOSTS=.railway.app,.onrender.com`
- [x] `DATABASE_URL=<auto-provided-by-platform>`
- [x] `CORS_ALLOWED_ORIGINS=<your-frontend-urls>`

## 🚀 Render Deployment Steps

### Step 1: Create PostgreSQL Database

1. Log into Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Configure database:
   - Name: `chargecast-db`
   - Database: `chargecast`
   - Region: Choose closest to users
   - Plan: Free or paid
4. **Save the Internal Database URL**

### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect GitHub repository
3. Configure:
   - **Name**: `chargecast-backend`
   - **Region**: Same as database
   - **Branch**: `main` or `master`
   - **Root Directory**: (leave blank)
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn chargecast_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`

### Step 3: Set Environment Variables

In Web Service Settings → Environment:

```bash
DEBUG=False
SECRET_KEY=<generate-using-django-command>
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<from-step-1-or-linked-database>
CARBON_INTENSITY_BASE_URL=https://api.carbonintensity.org.uk
CORS_ALLOWED_ORIGINS=<your-frontend-url>
```

**Generate SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Step 4: Deploy

- Click "Create Web Service"
- Monitor deployment logs
- Wait for "Live" status

### Step 5: Verify Deployment

```bash
# Health check
curl https://your-app.onrender.com/api/v1/health/

# Expected: {"status":"ok"}
```

## 🚂 Railway Deployment Steps

### Step 1: Create New Project

1. Log into Railway
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose `chargecast-backend` repository

### Step 2: Add PostgreSQL

1. In project, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Railway auto-sets `DATABASE_URL`

### Step 3: Configure Environment Variables

In Service Settings → Variables:

```bash
DEBUG=False
SECRET_KEY=<generate-using-django-command>
ALLOWED_HOSTS=.railway.app
CARBON_INTENSITY_BASE_URL=https://api.carbonintensity.org.uk
CORS_ALLOWED_ORIGINS=<your-frontend-url>
```

**Note:** `DATABASE_URL` is automatically set by Railway when you add PostgreSQL.

### Step 4: Generate Domain

1. Go to Settings
2. Click "Generate Domain"
3. Copy your Railway URL (e.g., `your-app.up.railway.app`)

### Step 5: Deploy

- Railway auto-deploys on push to main
- Or click "Deploy" manually
- Monitor deployment logs

### Step 6: Verify Deployment

```bash
# Health check
curl https://your-app.up.railway.app/api/v1/health/

# Expected: {"status":"ok"}
```

## 🔍 Common Issues & Solutions

### Issue: 502 Bad Gateway

**Possible Causes:**

1. **Database not connected**
   - ✅ Solution: Add PostgreSQL service
   - ✅ Verify `DATABASE_URL` is set
   - ✅ Check database logs

2. **Migrations failed**
   - ✅ Solution: Check deployment logs for migration errors
   - ✅ Verify database permissions
   - ✅ Check for model conflicts

3. **Gunicorn not starting**
   - ✅ Solution: Check if `gunicorn` is in requirements.txt
   - ✅ Verify `Procfile` or start command is correct
   - ✅ Check for port binding issues

4. **Environment variables missing**
   - ✅ Solution: Verify all required env vars are set
   - ✅ Especially `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`

### Issue: Static Files Not Loading

**Solutions:**
- ✅ Verify `collectstatic` ran in build logs
- ✅ Check `STATIC_ROOT` is set in settings.py
- ✅ Ensure WhiteNoise is in MIDDLEWARE
- ✅ Verify `STORAGES` configuration

### Issue: CORS Errors

**Solutions:**
- ✅ Add frontend URL to `CORS_ALLOWED_ORIGINS`
- ✅ Verify `corsheaders` in INSTALLED_APPS
- ✅ Check `CorsMiddleware` is first in MIDDLEWARE
- ✅ Set `CSRF_TRUSTED_ORIGINS` for POST requests

### Issue: Database Connection Errors

**Solutions:**
- ✅ Verify `DATABASE_URL` is set correctly
- ✅ Check database is in same region as web service
- ✅ Ensure `psycopg2-binary` is installed
- ✅ Verify `dj-database-url` is parsing URL correctly

### Issue: Build Fails

**Solutions:**
- ✅ Check build logs for specific error
- ✅ Verify `requirements.txt` has all dependencies
- ✅ Ensure Python version is compatible
- ✅ Check for syntax errors in code

## 📋 Post-Deployment Verification

After deployment, test these endpoints:

### 1. Health Check
```bash
curl https://your-app-url/api/v1/health/
# Expected: {"status":"ok"}
```

### 2. Root Endpoint
```bash
curl https://your-app-url/
# Expected: {"status":"ok"}
```

### 3. API Endpoints
```bash
# Current intensity
curl "https://your-app-url/api/v1/carbon/regional/current-30m/?postcode=SW1A1AA"

# 7-day history
curl "https://your-app-url/api/v1/carbon/regional/history-7d/?postcode=SW1A1AA"

# 48-hour forecast
curl "https://your-app-url/api/v1/carbon/regional/forecast-48h/?postcode=SW1A1AA"
```

### 4. Admin Panel (Optional)
```bash
# Visit in browser
https://your-app-url/admin/
```

## 🔐 Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` restricted to your domains
- [ ] `CORS_ALLOWED_ORIGINS` restricted to your frontend
- [ ] `.env` file in `.gitignore` (never commit secrets)
- [ ] Database credentials secure
- [ ] HTTPS enabled (automatic on Render/Railway)
- [ ] `CSRF_TRUSTED_ORIGINS` set correctly

## 📊 Monitoring

### Check Deployment Logs

**Render:**
- Dashboard → Your Service → Logs

**Railway:**
- Project → Service → Deployments → View Logs

### Look for:
- ✅ "Migrations applied successfully"
- ✅ "X static files copied to..."
- ✅ "Booting worker with pid..."
- ✅ "Listening at: http://0.0.0.0:XXXX"
- ❌ Any ERROR or CRITICAL messages

## 🔄 Automatic Deploys

Both platforms support auto-deploy on git push:

**Render:**
- Settings → Auto-Deploy: ON
- Pushes to main branch auto-deploy

**Railway:**
- Enabled by default
- Push to main → auto-deploy

## 🆘 Troubleshooting Commands

### Railway CLI

```bash
# Install
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs

# Run migrations manually
railway run python manage.py migrate

# Access shell
railway run python manage.py shell
```

### Render

- No CLI available
- Use web dashboard for all operations
- Check "Shell" tab for manual commands

## 📚 Additional Resources

- [Render Django Deployment Guide](https://render.com/docs/deploy-django)
- [Railway Python Documentation](https://docs.railway.app/guides/python)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

---

**Last Updated:** November 2025

**Status:** Ready for deployment to Render or Railway ✅
