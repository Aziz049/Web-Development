@echo off
echo ========================================
echo Pushing Clinic Appointment Manager to GitHub
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    echo Then restart this script.
    pause
    exit /b 1
)

echo Step 1: Initializing git repository...
git init

echo.
echo Step 2: Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/Aziz049/Web-Development.git

echo.
echo Step 3: Adding all files...
git add .

echo.
echo Step 4: Committing changes...
git commit -m "Initial commit: Clinic Appointment Manager with Django + DRF"

echo.
echo Step 5: Setting branch to main...
git branch -M main

echo.
echo Step 6: Pushing to GitHub...
echo NOTE: You will be prompted for your GitHub credentials.
echo Use your Personal Access Token as the password.
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Push failed. This might be due to:
    echo 1. Authentication issues - use a Personal Access Token
    echo 2. Repository doesn't exist or you don't have access
    echo 3. Network issues
    echo.
    echo See GIT_SETUP.md for detailed instructions.
) else (
    echo.
    echo SUCCESS! Your code has been pushed to GitHub!
    echo Repository: https://github.com/Aziz049/Web-Development
)

pause

