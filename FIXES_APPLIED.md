# Railway Deployment - 502 Error Fixes Applied

## Changes Made to Fix 502 Errors

### 1. **Database Configuration (settings.py)**
- ✅ Added support for Railway's `DATABASE_URL` environment variable
- ✅ Added `dj-database-url` package to parse Railway's database URL
- ✅ Maintains backward compatibility with individual DB environment variables for local development
- ✅ Added connection pooling (`conn_max_age=600`) for better performance
- ✅ Added connection health checks

### 2. **Dependencies (requirements.txt)**
- ✅ Added `dj-database-url==2.2.0` to parse PostgreSQL connection strings

### 3. **Gunicorn Configuration (Procfile)**
- ✅ Optimized worker/thread configuration for Railway's resources
- ✅ Changed to 2 workers with 4 threads each (better for Railway's typical container resources)
- ✅ Added 120-second timeout for long-running requests
- ✅ Added detailed logging (access-logfile, error-logfile, log-level info)

### 4. **CORS Configuration (settings.py)**
- ✅ Fixed CORS_ALLOWED_ORIGINS to properly handle empty strings
- ✅ Prevents errors when CORS_ALLOWED_ORIGINS is not set

### 5. **Railway-Specific Files**
- ✅ Created `railway.json` for Railway-specific build/deploy configuration
- ✅ Created `RAILWAY_DEPLOYMENT.md` with comprehensive deployment guide
- ✅ Updated `.env.example` with Railway-specific instructions

## What Was Causing the 502 Errors?

The most likely causes were:

1. **Database Connection Failure** ⭐ (MOST LIKELY)
   - Railway provides `DATABASE_URL`, but your app was looking for individual env vars
   - Without database connectivity, Django fails to start → 502 error

2. **Missing Environment Variables**
   - If `SECRET_KEY`, `ALLOWED_HOSTS`, or other critical vars weren't set

3. **Gunicorn Configuration**
   - Too many workers for Railway's resources could cause OOM errors
   - Missing timeout could cause request failures

## What to Do Next on Railway

### Immediate Steps:

1. **Ensure PostgreSQL is Added:**
   - In your Railway project, click "+ New" → "Database" → "Add PostgreSQL"
   - This automatically sets `DATABASE_URL`

2. **Set Environment Variables in Railway:**
   ```
   DEBUG=False
   SECRET_KEY=<generate using: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'>
   ALLOWED_HOSTS=.railway.app
   ```

3. **Commit and Push Changes:**
   ```bash
   git add .
   git commit -m "Fix Railway deployment: add DATABASE_URL support and optimize config"
   git push origin main
   ```

4. **Railway will auto-redeploy** (if auto-deploy is enabled)
   - Or manually trigger a deployment in Railway dashboard

### Verification Steps:

1. **Check Deployment Logs:**
   - Look for successful migration messages
   - Verify no database connection errors
   - Confirm gunicorn starts successfully

2. **Test Health Endpoint:**
   ```bash
   curl https://your-app.railway.app/api/v1/health/
   ```
   Should return: `{"status":"ok"}`

3. **Test API Endpoints:**
   ```bash
   curl "https://your-app.railway.app/api/v1/carbon/regional/current-30m/?postcode=SW1A1AA"
   ```

## If Still Getting 502 Errors:

1. **Check Railway Logs:**
   - Go to your service in Railway
   - Click "Deployments" → Latest deployment → View logs
   - Look for error messages

2. **Common Issues:**
   - Database not connected → Add PostgreSQL service
   - Missing SECRET_KEY → Set in environment variables
   - Migration errors → Check database permissions
   - Out of memory → Reduce workers in Procfile

3. **Get More Details:**
   - Railway logs will show the exact error
   - Share the error message for more specific help

## Files Modified:

- ✅ `chargecast_backend/settings.py` - Database & CORS fixes
- ✅ `requirements.txt` - Added dj-database-url
- ✅ `Procfile` - Optimized gunicorn config
- ✅ `.env.example` - Updated with Railway instructions
- ✅ `railway.json` - New Railway config file
- ✅ `RAILWAY_DEPLOYMENT.md` - New comprehensive guide

## Testing Locally (Optional):

If you want to test the changes locally:

```bash
# Install new dependency
pip install -r requirements.txt

# Set DATABASE_URL in your terminal (example)
export DATABASE_URL="postgresql://user:password@localhost:5432/chargecast"

# Or continue using individual DB env vars in .env file
# (The code supports both approaches)

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

---

**These changes should resolve your 502 errors.** The main issue was that Railway provides `DATABASE_URL` but your app wasn't configured to use it. Now it supports both Railway's approach and local development with individual env vars.
