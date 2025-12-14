# PowerShell script to push project to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Pushing Clinic Appointment Manager to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version 2>&1
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Then restart this script." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Step 1: Initializing git repository..." -ForegroundColor Yellow
git init

Write-Host ""
Write-Host "Step 2: Adding remote repository..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/Aziz049/Web-Development.git

Write-Host ""
Write-Host "Step 3: Adding all files..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "Step 4: Committing changes..." -ForegroundColor Yellow
git commit -m "Initial commit: Clinic Appointment Manager with Django + DRF"

Write-Host ""
Write-Host "Step 5: Setting branch to main..." -ForegroundColor Yellow
git branch -M main

Write-Host ""
Write-Host "Step 6: Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "NOTE: You will be prompted for your GitHub credentials." -ForegroundColor Cyan
Write-Host "Use your Personal Access Token as the password." -ForegroundColor Cyan
Write-Host ""

$pushResult = git push -u origin main 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Push failed. This might be due to:" -ForegroundColor Red
    Write-Host "1. Authentication issues - use a Personal Access Token" -ForegroundColor Yellow
    Write-Host "2. Repository doesn't exist or you don't have access" -ForegroundColor Yellow
    Write-Host "3. Network issues" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "See GIT_SETUP.md for detailed instructions." -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "SUCCESS! Your code has been pushed to GitHub!" -ForegroundColor Green
    Write-Host "Repository: https://github.com/Aziz049/Web-Development" -ForegroundColor Cyan
}

Read-Host "Press Enter to exit"

