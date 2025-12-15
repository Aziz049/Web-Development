# Install Heroku CLI First

## Step 1: Install Heroku

**Run the installer:**
```
C:\Users\USER\Downloads\heroku-x64.exe
```

1. Double-click the file
2. Follow installation wizard
3. **Restart your terminal/PowerShell** after installation

## Step 2: Verify Installation

Open a **NEW** terminal and run:
```powershell
heroku --version
```

If you see a version number, installation was successful!

## Step 3: Deploy

After installation, run:
```powershell
.\DEPLOY_NOW.ps1
```

Or manually:
```powershell
heroku login
heroku create apex-dental-appointment-manager
git push heroku main
heroku run python manage.py migrate
```

---

**Note:** You MUST restart your terminal after installing Heroku for it to work!

