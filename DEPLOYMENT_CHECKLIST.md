# Railway Deployment Checklist

## ✅ Pre-Deployment Verification

### 1. Python Version
- [x] `runtime.txt` contains `python-3.10.13`
- [x] No Python 3.11 references in project
- [x] No `.python-version` file
- [x] No `.mise.toml` file

### 2. Requirements
- [x] `requirements.txt` contains:
  - [x] Django==4.2.7
  - [x] djangorestframework==3.14.0
  - [x] gunicorn==21.2.0
  - [x] psycopg2-binary>=2.9.5
  - [x] dj-database-url>=2.1.0
  - [x] whitenoise==6.6.0

### 3. Production Server
- [x] `Procfile` uses gunicorn
- [x] `Procfile` binds to `0.0.0.0:$PORT`
- [x] `railway.json` has correct start command
- [x] `railway.toml` has correct start command

### 4. Database Configuration
- [x] `settings.py` reads `DATABASE_URL` from environment
- [x] Uses `dj_database_url.parse()` for Railway
- [x] Falls back to SQLite for local development

### 5. Static Files
- [x] `STATIC_ROOT` is set to `BASE_DIR / 'staticfiles'`
- [x] `STATICFILES_STORAGE` uses WhiteNoise
- [x] WhiteNoise middleware is in `MIDDLEWARE`
- [x] `collectstatic` will run automatically

### 6. Environment Variables
- [x] `SECRET_KEY` read from environment
- [x] `DEBUG` read from environment (defaults to False in production)
- [x] `ALLOWED_HOSTS` supports Railway domains
- [x] `DATABASE_URL` automatically provided by Railway

### 7. Security Settings
- [x] Production security settings enabled when `DEBUG=False`
- [x] HTTPS redirect configured
- [x] Secure cookies enabled
- [x] HSTS headers configured
- [x] CORS configured for Railway domains
- [x] CSRF trusted origins configured

### 8. Django Configuration
- [x] System check passes: `python manage.py check`
- [x] No migration issues
- [x] All apps properly configured

## 🚀 Deployment Steps

1. **Commit Changes**
   ```bash
   git add runtime.txt DEPLOYMENT_GUIDE.md
   git commit -m "Fix Railway deployment: Use Python 3.10.13"
   git push origin main
   ```

2. **Railway Will Automatically**
   - Detect `runtime.txt` with Python 3.10.13
   - Build the application
   - Install dependencies
   - Start with gunicorn

3. **Set Environment Variables in Railway**
   - `SECRET_KEY` (generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app-name.up.railway.app`
   - `DATABASE_URL` (automatically set when PostgreSQL is added)

4. **Run Migrations**
   - Use Railway shell or CLI
   - Run: `python manage.py migrate`

5. **Create Superuser**
   - Run: `python manage.py createsuperuser`

## ✅ Post-Deployment Verification

- [ ] Build succeeds without errors
- [ ] Application starts successfully
- [ ] Home page loads: `https://your-app-name.up.railway.app/`
- [ ] API docs accessible: `https://your-app-name.up.railway.app/api/docs/`
- [ ] Admin panel accessible: `https://your-app-name.up.railway.app/admin/`
- [ ] Patient registration works
- [ ] JWT login works
- [ ] Appointment booking works
- [ ] Static files load correctly
- [ ] No 500 errors in logs

## 🔍 Troubleshooting

### Build Fails
- Check Railway logs for specific error
- Verify `runtime.txt` is `python-3.10.13`
- Verify `requirements.txt` is correct

### Application Won't Start
- Check `Procfile` is correct
- Verify environment variables are set
- Check Railway logs for errors

### Database Connection Fails
- Verify PostgreSQL service is running
- Check `DATABASE_URL` is set (Railway sets this automatically)
- Run migrations: `python manage.py migrate`

### Static Files 404
- Check `collectstatic` ran during build
- Verify WhiteNoise middleware is enabled
- Check `STATIC_ROOT` is correct

---

**Status**: ✅ Ready for Railway Deployment


