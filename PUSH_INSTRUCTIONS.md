# Push to GitHub - Step by Step Instructions

## ⚠️ SECURITY WARNING
**DO NOT commit your Personal Access Token to the repository!**
The token you provided should be kept secret and only used for authentication.

## Step 1: Install Git (if not already installed)

1. Download Git for Windows: https://git-scm.com/download/win
2. Install with default settings
3. **Restart your terminal/PowerShell** after installation

## Step 2: Verify Git Installation

Open PowerShell and run:
```powershell
git --version
```

You should see something like: `git version 2.x.x`

## Step 3: Navigate to Project Directory

```powershell
cd "C:\Users\USER\Downloads\Web Development final project]"
```

## Step 4: Initialize Git and Push

Run these commands one by one:

```powershell
# Initialize git repository
git init

# Add remote repository
git remote add origin https://github.com/Aziz049/Web-Development.git

# Add all files (respects .gitignore)
git add .

# Commit changes
git commit -m "Initial commit: Clinic Appointment Manager with Django + DRF"

# Set branch to main
git branch -M main

# Push to GitHub
# When prompted for username: enter "Aziz049"
# When prompted for password: paste your Personal Access Token
git push -u origin main
```

## Alternative: Use Token in URL (One-time push)

If you prefer, you can include the token in the URL for the first push:

```powershell
git init
git remote add origin https://YOUR_TOKEN@github.com/Aziz049/Web-Development.git
git add .
git commit -m "Initial commit: Clinic Appointment Manager with Django + DRF"
git branch -M main
git push -u origin main
```

**Note**: After the first push, remove the token from the remote URL:
```powershell
git remote set-url origin https://github.com/Aziz049/Web-Development.git
```

## Troubleshooting

### If you get "remote origin already exists":
```powershell
git remote remove origin
git remote add origin https://github.com/Aziz049/Web-Development.git
```

### If you get authentication errors:
- Make sure you're using the token (not your GitHub password)
- Check that the token hasn't expired
- Verify the repository exists and you have access

### If push is rejected:
The repository might have existing content. Use:
```powershell
git push -u origin main --force
```
⚠️ **Warning**: `--force` will overwrite existing content in the repository.

## After Successful Push

1. Verify on GitHub: https://github.com/Aziz049/Web-Development
2. Consider revoking and regenerating the token for security
3. Never commit the token to your repository

