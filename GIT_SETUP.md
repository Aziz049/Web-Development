# Git Setup and Push Instructions

## Step 1: Install Git (if not installed)

If Git is not installed on your system:

1. **Download Git for Windows**: https://git-scm.com/download/win
2. Install it with default settings
3. Restart your terminal/PowerShell after installation

## Step 2: Configure Git (First time only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Initialize Git and Push to GitHub

Run these commands in your project directory:

```bash
# Navigate to project directory
cd "C:\Users\USER\Downloads\Web Development final project]"

# Initialize git repository
git init

# Add remote repository
git remote add origin https://github.com/Aziz049/Web-Development.git

# Add all files (respects .gitignore)
git add .

# Commit changes
git commit -m "Initial commit: Clinic Appointment Manager with Django + DRF"

# Push to GitHub
git push -u origin main
```

**Note**: If the default branch is `master` instead of `main`, use:
```bash
git branch -M main
git push -u origin main
```

## Step 4: Authentication

When you push, GitHub will ask for authentication. You have two options:

### Option A: Personal Access Token (Recommended)
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with `repo` permissions
3. Use the token as your password when prompted

### Option B: GitHub CLI
```bash
# Install GitHub CLI, then:
gh auth login
```

## Troubleshooting

### If you get "remote origin already exists":
```bash
git remote remove origin
git remote add origin https://github.com/Aziz049/Web-Development.git
```

### If you get authentication errors:
- Make sure you're using a Personal Access Token (not your GitHub password)
- Or use SSH instead: `git remote set-url origin git@github.com:Aziz049/Web-Development.git`

### If you need to update later:
```bash
git add .
git commit -m "Your commit message"
git push
```

