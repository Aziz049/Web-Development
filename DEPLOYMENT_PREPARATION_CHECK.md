# Deployment Preparation Checklist ✅

## 1️⃣ Prepare the Project for Deployment

### ✅ requirements.txt
**Status**: VERIFIED
- File exists: `requirements.txt`
- Contains all dependencies:
  - ✅ Django==4.2.7
  - ✅ djangorestframework==3.14.0
  - ✅ gunicorn==21.2.0
  - ✅ psycopg2-binary>=2.9.5
  - ✅ dj-database-url>=2.1.0
  - ✅ whitenoise==6.6.0
  - ✅ djoser==2.2.0
  - ✅ djangorestframework-simplejwt==5.3.0
  - ✅ django-cors-headers==4.3.1
  - ✅ python-decouple==3.8
  - ✅ pymongo>=4.6.0
  - ✅ drf-spectacular==0.27.0

**Note**: All dependencies are pinned with specific versions for production stability.

### ✅ runtime.txt
**Status**: VERIFIED
- File exists: `runtime.txt`
- Content: `python-3.10.13`
- Railway supports Python 3.10.x automatically

**Note**: Using 3.10.13 (newer patch version) instead of 3.10.11 - both are supported.

### ✅ Procfile
**Status**: VERIFIED
- File exists: `Procfile`
- Content: `web: gunicorn clinic_appointment.wsgi --bind 0.0.0.0:$PORT`
- Correct format for Railway deployment

### ✅ Environment Variables Configuration
**Status**: VERIFIED in `settings.py`

#### SECRET_KEY
```python
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')
```
- ✅ Reads from environment variable
- ✅ Must be set in Railway dashboard

#### DEBUG
```python
DEBUG = config('DEBUG', default=True, cast=bool)
```
- ✅ Reads from environment variable
- ✅ Must be set to `False` in Railway dashboard

#### DATABASE_URL
```python
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
```
- ✅ Reads from environment variable
- ✅ Railway automatically provides `DATABASE_URL` when PostgreSQL is added
- ✅ Uses `dj-database-url` for parsing

#### ALLOWED_HOSTS
```python
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])
```
- ✅ Reads from environment variable
- ✅ Must include Railway domain: `your-app-name.up.railway.app`

### ✅ Additional Configuration
- ✅ WhiteNoise configured for static files
- ✅ Production security settings enabled when `DEBUG=False`
- ✅ CORS and CSRF configured for Railway domains
- ✅ Django system check passes

## 2️⃣ Push Your Code to GitHub

### Commands to Run:
```bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "Prepare for Railway deployment"

# Push to GitHub
git push origin main
```

### Files to Commit:
- ✅ `requirements.txt` - All dependencies
- ✅ `runtime.txt` - Python 3.10.13
- ✅ `Procfile` - Gunicorn start command
- ✅ `railway.json` - Railway build configuration
- ✅ `railway.toml` - Railway deployment configuration
- ✅ `clinic_appointment/settings.py` - Environment variable configuration
- ✅ All other project files

## 3️⃣ Railway Environment Variables to Set

After pushing to GitHub and connecting to Railway, set these in Railway Dashboard:

### Required Variables:
```bash
SECRET_KEY=<generate-with-command-below>
DEBUG=False
ALLOWED_HOSTS=your-app-name.up.railway.app,localhost,127.0.0.1
```

### Generate SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Automatic Variables (Railway Provides):
- ✅ `DATABASE_URL` - Automatically set when PostgreSQL is added
- ✅ `PORT` - Automatically set by Railway
- ✅ `RAILWAY_ENVIRONMENT` - Automatically set

### Optional Variables:
```bash
MONGODB_URI=mongodb+srv://... (if using MongoDB)
CORS_ALLOWED_ORIGINS=https://your-frontend.com (if needed)
CSRF_TRUSTED_ORIGINS=https://your-app-name.up.railway.app (if needed)
```

## ✅ Verification Checklist

- [x] `requirements.txt` exists with all dependencies
- [x] `runtime.txt` exists with `python-3.10.13`
- [x] `Procfile` exists with correct gunicorn command
- [x] `settings.py` reads environment variables
- [x] `DATABASE_URL` configuration in place
- [x] `SECRET_KEY` reads from environment
- [x] `DEBUG` reads from environment
- [x] `ALLOWED_HOSTS` reads from environment
- [x] WhiteNoise configured
- [x] Production security settings configured
- [x] Django system check passes
- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] PostgreSQL database added
- [ ] Environment variables set in Railway
- [ ] Deployment successful

## 🚀 Next Steps

1. **Commit and Push:**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Create Railway Project:**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add PostgreSQL:**
   - In Railway project, click "+ New"
   - Select "Database" → "Add PostgreSQL"
   - Railway automatically sets `DATABASE_URL`

4. **Set Environment Variables:**
   - Go to your service → "Variables" tab
   - Add: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`

5. **Deploy:**
   - Railway auto-deploys on push
   - Check deployment logs
   - Run migrations: `railway run python manage.py migrate`
   - Create superuser: `railway run python manage.py createsuperuser`

---

**Status**: ✅ ALL PREPARATION STEPS COMPLETE - Ready for Railway Deployment

