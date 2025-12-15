# Heroku Deployment Script
# Run this AFTER installing Heroku CLI

Write-Host "=== Heroku Deployment ===" -ForegroundColor Green

# Try to find Heroku
$herokuPath = $null
$paths = @(
    "$env:LOCALAPPDATA\Programs\heroku\bin\heroku.exe",
    "$env:ProgramFiles\Heroku\bin\heroku.exe",
    "$env:USERPROFILE\AppData\Local\Programs\heroku\bin\heroku.exe"
)

foreach ($path in $paths) {
    if (Test-Path $path) {
        $herokuPath = $path
        Write-Host "Found Heroku at: $path" -ForegroundColor Green
        break
    }
}

if (-not $herokuPath) {
    Write-Host "ERROR: Heroku not found!" -ForegroundColor Red
    Write-Host "Please install Heroku first:" -ForegroundColor Yellow
    Write-Host "1. Run: C:\Users\USER\Downloads\heroku-x64.exe" -ForegroundColor Yellow
    Write-Host "2. Restart terminal" -ForegroundColor Yellow
    Write-Host "3. Run this script again" -ForegroundColor Yellow
    exit 1
}

# Step 1: Login
Write-Host "`n[1/7] Logging into Heroku..." -ForegroundColor Cyan
& $herokuPath login

# Step 2: Create app
Write-Host "`n[2/7] Creating Heroku app..." -ForegroundColor Cyan
& $herokuPath create apex-dental-appointment-manager

# Step 3: Generate secret key
Write-Host "`n[3/7] Generating secret key..." -ForegroundColor Cyan
$secretKey = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Step 4: Set environment variables
Write-Host "`n[4/7] Setting environment variables..." -ForegroundColor Cyan
& $herokuPath config:set SECRET_KEY="$secretKey"
& $herokuPath config:set DEBUG=False
& $herokuPath config:set ALLOWED_HOSTS="apex-dental-appointment-manager.herokuapp.com"

# Step 5: Add PostgreSQL
Write-Host "`n[5/7] Adding PostgreSQL database..." -ForegroundColor Cyan
& $herokuPath addons:create heroku-postgresql:mini

# Step 6: Deploy
Write-Host "`n[6/7] Deploying to Heroku..." -ForegroundColor Cyan
git push heroku main

# Step 7: Run migrations
Write-Host "`n[7/7] Running migrations..." -ForegroundColor Cyan
& $herokuPath run python manage.py migrate

# Collect static files
Write-Host "`nCollecting static files..." -ForegroundColor Cyan
& $herokuPath run python manage.py collectstatic --noinput

# Open app
Write-Host "`nOpening your app..." -ForegroundColor Cyan
& $herokuPath open

Write-Host "`n=== DEPLOYMENT COMPLETE! ===" -ForegroundColor Green
Write-Host "Your app: https://apex-dental-appointment-manager.herokuapp.com" -ForegroundColor Green
Write-Host "`nNext: Create superuser with: heroku run python manage.py createsuperuser" -ForegroundColor Yellow

