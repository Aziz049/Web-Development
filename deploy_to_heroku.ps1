# Heroku Deployment Script
# Run this script after finding your Heroku installation path

Write-Host "=== Heroku Deployment Script ===" -ForegroundColor Green

# Step 1: Find Heroku (uncomment and update the path if you know it)
# $herokuPath = "C:\Users\USER\AppData\Local\Programs\heroku\bin\heroku.exe"

# Or try to find it automatically
$possiblePaths = @(
    "$env:LOCALAPPDATA\Programs\heroku\bin\heroku.exe",
    "$env:ProgramFiles\Heroku\bin\heroku.exe",
    "$env:USERPROFILE\AppData\Local\Programs\heroku\bin\heroku.exe"
)

$herokuPath = $null
foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $herokuPath = $path
        Write-Host "Found Heroku at: $herokuPath" -ForegroundColor Green
        break
    }
}

if (-not $herokuPath) {
    Write-Host "Heroku CLI not found. Please:" -ForegroundColor Red
    Write-Host "1. Install from: https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Yellow
    Write-Host "2. Or find the installation path and update this script" -ForegroundColor Yellow
    exit 1
}

# Step 2: Login
Write-Host "`nStep 1: Logging into Heroku..." -ForegroundColor Cyan
& $herokuPath login

# Step 3: Create app
Write-Host "`nStep 2: Creating Heroku app..." -ForegroundColor Cyan
& $herokuPath create apex-dental-appointment-manager

# Step 4: Generate and set secret key
Write-Host "`nStep 3: Generating secret key..." -ForegroundColor Cyan
$secretKey = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
Write-Host "Secret key generated!" -ForegroundColor Green

Write-Host "`nStep 4: Setting environment variables..." -ForegroundColor Cyan
& $herokuPath config:set SECRET_KEY="$secretKey"
& $herokuPath config:set DEBUG=False
& $herokuPath config:set ALLOWED_HOSTS="apex-dental-appointment-manager.herokuapp.com"

# Step 5: Add PostgreSQL
Write-Host "`nStep 5: Adding PostgreSQL database..." -ForegroundColor Cyan
& $herokuPath addons:create heroku-postgresql:mini

# Step 6: Deploy
Write-Host "`nStep 6: Deploying to Heroku..." -ForegroundColor Cyan
git push heroku main

# Step 7: Run migrations
Write-Host "`nStep 7: Running migrations..." -ForegroundColor Cyan
& $herokuPath run python manage.py migrate

# Step 8: Collect static files
Write-Host "`nStep 8: Collecting static files..." -ForegroundColor Cyan
& $herokuPath run python manage.py collectstatic --noinput

# Step 9: Open app
Write-Host "`nStep 9: Opening your app..." -ForegroundColor Cyan
& $herokuPath open

Write-Host "`n=== Deployment Complete! ===" -ForegroundColor Green
Write-Host "Your app is live at: https://apex-dental-appointment-manager.herokuapp.com" -ForegroundColor Green

