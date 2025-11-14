# Deployment Guide for Render

## Prerequisites

1. A GitHub repository with your code
2. A Render account (https://render.com)
3. Your code committed and pushed to GitHub

## Steps to Deploy on Render

### 1. Create a PostgreSQL Database

1. Log in to your Render dashboard
2. Click "New +" and select "PostgreSQL"
3. Configure your database:
   - **Name**: `chargecast-db` (or your preferred name)
   - **Database**: `chargecast`
   - **User**: (auto-generated)
   - **Region**: Choose closest to your users
   - **PostgreSQL Version**: 16 (or latest)
   - **Plan**: Free (or as needed)
4. Click "Create Database"
5. **Save the connection details** - you'll need the Internal Database URL

### 2. Create a Web Service

1. Click "New +" and select "Web Service"
2. Connect your GitHub repository
3. Configure your web service:
   - **Name**: `chargecast-backend` (or your preferred name)
   - **Region**: Same as your database
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave blank (unless repo has subdirectories)
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn chargecast_backend.wsgi:application`
   - **Plan**: Free (or as needed)

### 3. Set Environment Variables

In the web service settings, add these environment variables:

```
DEBUG=False
SECRET_KEY=<generate-a-secure-random-key>
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<internal-database-url-from-step-1>
CARBON_INTENSITY_BASE_URL=https://api.carbonintensity.org.uk
CORS_ALLOWED_ORIGINS=<your-frontend-url-if-any>
```

**Important Notes:**
- For `SECRET_KEY`, generate a secure random string (50+ characters)
- Use Python to generate one: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- Render automatically sets `DATABASE_URL` if you link the database
- If you link the database in Render, you don't need to set individual DB_* variables

### 4. Update settings.py for DATABASE_URL (Optional but Recommended)

If using Render's DATABASE_URL, install `dj-database-url`:

```bash
pip install dj-database-url
```

Then update your `settings.py`:

```python
import dj_database_url

# Replace the DATABASES configuration with:
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}
```

Don't forget to update requirements.txt after installing dj-database-url.

### 5. Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Run `./build.sh` (installs dependencies, collects static files, runs migrations)
   - Start your application with gunicorn

### 6. Monitor Deployment

- Check the "Logs" tab to monitor the build and deployment process
- Once deployed, your API will be available at: `https://your-service-name.onrender.com`

## Post-Deployment Checklist

- [ ] Test your API endpoints
- [ ] Verify database connections
- [ ] Check static files are served correctly
- [ ] Test CORS settings with your frontend
- [ ] Monitor logs for any errors
- [ ] Set up custom domain (optional)
- [ ] Configure health checks in Render settings

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure `build.sh` has execute permissions
- Verify all dependencies are in `requirements.txt`

### Database Connection Issues
- Verify DATABASE_URL is set correctly
- Check database is in the same region as web service
- Ensure migrations ran successfully

### Static Files Not Loading
- Check `STATIC_ROOT` and `STATIC_URL` in settings
- Verify `collectstatic` ran in build script
- Ensure WhiteNoise is installed and configured

### CORS Errors
- Add your frontend URL to `CORS_ALLOWED_ORIGINS`
- Verify corsheaders is installed and in INSTALLED_APPS

## Important Security Notes

1. **Never commit `.env` file** - it's in `.gitignore`
2. **Use strong SECRET_KEY** - generate a new one for production
3. **Set DEBUG=False** in production
4. **Configure ALLOWED_HOSTS** properly
5. **Use HTTPS** for production (Render provides this automatically)
6. **Restrict CORS** - only allow your frontend domain(s)

## Automatic Deploys

Render can automatically deploy when you push to GitHub:
1. Go to your web service settings
2. Enable "Auto-Deploy" for your main branch
3. Every push to main will trigger a new deployment
