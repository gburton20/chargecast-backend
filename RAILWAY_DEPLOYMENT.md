# Railway Deployment Guide for ChargeCast Backend

## Prerequisites

1. A GitHub repository with your code (already done)
2. A Railway account (https://railway.app)
3. Code committed and pushed to GitHub

## Quick Deployment Steps

### 1. Create a New Project on Railway

1. Log in to Railway (https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub account if needed
5. Select your `chargecast-backend` repository

### 2. Add PostgreSQL Database

1. In your Railway project, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will automatically create the database and set the `DATABASE_URL` environment variable

### 3. Configure Environment Variables

In your Railway service settings, add these environment variables:

**Required Variables:**
```
DEBUG=False
SECRET_KEY=<generate-a-secure-random-key>
ALLOWED_HOSTS=.railway.app
```

**Optional Variables (if you need CORS):**
```
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

**Important Notes:**
- `DATABASE_URL` is automatically set by Railway when you add PostgreSQL
- For `SECRET_KEY`, generate a secure random string (50+ characters)
  - Use: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- The app automatically detects Railway's environment

### 4. Deploy

Railway will automatically:
1. Detect it's a Python project
2. Install dependencies from `requirements.txt`
3. Run migrations
4. Collect static files
5. Start your application with gunicorn

### 5. Monitor Deployment

- Check the "Deployments" tab to see build logs
- Click on the latest deployment to view detailed logs
- Once deployed, click "Settings" → "Generate Domain" to get your public URL

## Common Issues and Solutions

### Issue: 502 Bad Gateway Error

**Causes & Solutions:**

1. **Database not connected:**
   - Ensure PostgreSQL service is added to your project
   - Verify `DATABASE_URL` is in environment variables
   - Check database connection in deployment logs

2. **Migrations failed:**
   - Check deployment logs for migration errors
   - Ensure database is accessible
   - May need to run migrations manually via Railway CLI

3. **Port binding issue:**
   - Railway automatically sets `PORT` environment variable
   - Ensure your `Procfile` uses `$PORT`
   - Current Procfile: `web: gunicorn chargecast_backend.wsgi --bind 0.0.0.0:$PORT ...`

4. **Static files not collected:**
   - Check if `collectstatic` ran successfully in build logs
   - Verify `STATIC_ROOT` is set in settings.py
   - Ensure WhiteNoise is in MIDDLEWARE

5. **Missing environment variables:**
   - Verify all required env vars are set in Railway dashboard
   - Especially `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS`

### Issue: Application Crashes on Startup

**Check these:**
- View deployment logs in Railway dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility (Python 3.12)
- Check for syntax errors in settings.py

### Issue: Database Connection Errors

**Solutions:**
- Ensure PostgreSQL service is running
- Verify `DATABASE_URL` is set (should be automatic)
- Check if migrations completed successfully
- Try redeploying the service

## Useful Railway Commands

If you install the Railway CLI:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# View logs
railway logs

# Run migrations manually
railway run python manage.py migrate

# Access Django shell
railway run python manage.py shell
```

## Health Check

After deployment, test your API:

```bash
# Health check endpoint
curl https://your-app.railway.app/api/v1/health/

# Expected response:
# {"status":"ok"}
```

## Testing Other Endpoints

```bash
# Test carbon intensity endpoint
curl "https://your-app.railway.app/api/v1/carbon/regional/current-30m/?postcode=SW1A1AA"
```

## Post-Deployment Checklist

- [ ] Service is deployed and running
- [ ] Database is connected and migrations are complete
- [ ] Environment variables are set correctly
- [ ] `/api/v1/health/` endpoint returns `{"status":"ok"}`
- [ ] API endpoints work correctly
- [ ] Static files are served (if using admin panel)
- [ ] CORS is configured for your frontend (if applicable)
- [ ] Logs show no errors

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Auto-set | - | PostgreSQL connection string (auto-set by Railway) |
| `DEBUG` | Yes | False | Set to False in production |
| `SECRET_KEY` | Yes | - | Django secret key (generate securely) |
| `ALLOWED_HOSTS` | Yes | - | Use `.railway.app` for Railway |
| `CORS_ALLOWED_ORIGINS` | No | - | Frontend domains (comma-separated) |
| `PORT` | Auto-set | - | Port number (auto-set by Railway) |

## Automatic Deploys

Railway automatically deploys when you push to your main branch:
- Push code to GitHub
- Railway detects changes
- Automatically builds and deploys

To disable automatic deploys:
1. Go to service settings
2. Under "Deployment" section
3. Toggle off "Auto Deploy"

## Troubleshooting Tips

1. **Always check the deployment logs first** - they contain detailed error messages
2. **Verify environment variables** - missing vars cause most deployment issues
3. **Test locally first** - ensure app works with PostgreSQL locally
4. **Check Railway status** - visit https://railway.app/status for service status
5. **Use Railway's built-in metrics** - CPU, memory, and network usage can reveal issues

## Rolling Back

If a deployment fails:
1. Go to "Deployments" tab
2. Find a previous successful deployment
3. Click "..." menu → "Redeploy"

## Support

- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Report bugs in your repository

---

**Last Updated:** November 2025
