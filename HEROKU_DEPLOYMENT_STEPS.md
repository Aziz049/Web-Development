# Heroku Deployment - Manual Steps

Since Heroku CLI needs to be in your PATH, follow these steps:

## Step 1: Add Heroku to PATH (if not already)

**Option A: Find Heroku Installation**
```powershell
# Check common locations
Test-Path "$env:LOCALAPPDATA\Programs\heroku\bin\heroku.exe"
Test-Path "$env:ProgramFiles\Heroku\bin\heroku.exe"
Test-Path "$env:USERPROFILE\AppData\Local\Programs\heroku\bin\heroku.exe"
```

**Option B: Add to PATH**
1. Find where Heroku is installed (usually `C:\Users\USER\AppData\Local\Programs\heroku\bin\`)
2. Add that path to Windows PATH environment variable
3. Restart terminal

## Step 2: Login to Heroku
```bash
heroku login
```

## Step 3: Create Heroku App
```bash
heroku create apex-dental-appointment-manager
```

## Step 4: Set Environment Variables
```bash
# Generate secret key first
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Then set it (replace with your generated key)
heroku config:set SECRET_KEY="your-generated-secret-key-here"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="apex-dental-appointment-manager.herokuapp.com"
```

## Step 5: Add PostgreSQL
```bash
heroku addons:create heroku-postgresql:mini
```

## Step 6: Deploy
```bash
git push heroku main
```

## Step 7: Run Migrations
```bash
heroku run python manage.py migrate
```

## Step 8: Create Superuser
```bash
heroku run python manage.py createsuperuser
```

## Step 9: Collect Static Files
```bash
heroku run python manage.py collectstatic --noinput
```

## Step 10: Open Your App
```bash
heroku open
```

---

## Alternative: Use Heroku Dashboard

If CLI doesn't work, you can deploy via:
1. **GitHub Integration**: Push to GitHub, connect to Heroku
2. **Heroku Dashboard**: https://dashboard.heroku.com/
   - Create new app
   - Connect GitHub repository
   - Enable automatic deploys

---

## Quick Check: Is Heroku Installed?

Run this to find Heroku:
```powershell
Get-ChildItem -Path "$env:LOCALAPPDATA\Programs" -Filter "heroku.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object FullName
```

