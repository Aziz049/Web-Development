# PowerShell script to push to GitHub using Personal Access Token
# SECURITY: This script uses a token - do NOT commit this file after first use!

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Pushing to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $null = git --version 2>&1
    Write-Host "Git found!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Then restart this script." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Your GitHub token (will be removed from remote after push)
# IMPORTANT: Replace YOUR_TOKEN_HERE with your actual token
$token = "YOUR_TOKEN_HERE"
$username = "Aziz049"
$repo = "Web-Development"

Write-Host "Step 1: Initializing git repository..." -ForegroundColor Yellow
if (Test-Path .git) {
    Write-Host "Git already initialized" -ForegroundColor Gray
} else {
    git init
}

Write-Host ""
Write-Host "Step 2: Configuring remote..." -ForegroundColor Yellow
git remote remove origin 2>$null
$remoteUrl = "https://${token}@github.com/${username}/${repo}.git"
git remote add origin $remoteUrl

Write-Host ""
Write-Host "Step 3: Adding all files..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "Step 4: Committing changes..." -ForegroundColor Yellow
git commit -m "Initial commit: Clinic Appointment Manager with Django + DRF" 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Commit successful" -ForegroundColor Green
} else {
    Write-Host "No changes to commit or commit failed" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 5: Setting branch to main..." -ForegroundColor Yellow
git branch -M main 2>&1 | Out-Null

Write-Host ""
Write-Host "Step 6: Pushing to GitHub..." -ForegroundColor Yellow
Write-Host ""

$pushOutput = git push -u origin main 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! Code pushed to GitHub!" -ForegroundColor Green
    Write-Host "Repository: https://github.com/${username}/${repo}" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Step 7: Removing token from remote URL for security..." -ForegroundColor Yellow
    git remote set-url origin "https://github.com/${username}/${repo}.git"
    Write-Host "Token removed from remote URL" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: Delete this script file (push_with_token.ps1) to keep your token secure!" -ForegroundColor Red
} else {
    Write-Host ""
    Write-Host "ERROR: Push failed!" -ForegroundColor Red
    Write-Host $pushOutput -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Possible issues:" -ForegroundColor Yellow
    Write-Host "1. Repository doesn't exist or you don't have access" -ForegroundColor Yellow
    Write-Host "2. Token is invalid or expired" -ForegroundColor Yellow
    Write-Host "3. Network connection issues" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Try: git push -u origin main --force" -ForegroundColor Cyan
    Write-Host "(Warning: --force will overwrite existing content)" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

