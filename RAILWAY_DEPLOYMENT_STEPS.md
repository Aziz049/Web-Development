# Railway Deployment Steps - Complete Guide

## 🚀 Deployment Status

✅ **Code Pushed to GitHub**: All changes committed and pushed  
✅ **Settings Updated**: ALLOWED_HOSTS includes `web-production-8531f.up.railway.app`  
✅ **Ready for Deployment**: Project is configured for Railway

---

## 📋 Two Deployment Methods

### Method 1: Railway Dashboard (Recommended - No CLI Needed)

Since Railway CLI is not installed, use the Railway Dashboard:

#### Step 1: Connect GitHub Repository
1. Go to https://railway.app
2. Log in with your account
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Authorize Railway to access your GitHub
6. Select repository: `Aziz049/Web-Development`

#### Step 2: Add PostgreSQL Database
1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway automatically:
   - Creates PostgreSQL database
   - Sets `DATABASE_URL` environment variable
   - Connects it to your service

#### Step 3: Set Environment Variables
1. Click on your **service** (Django app)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"** and add:

**Required Variables:**
```bash
SECRET_KEY=-i$kaay-4nd-k6xp58(h9l)gup@!=4hnl!-am582lz0nbl(s*s
DEBUG=False
ALLOWED_HOSTS=web-production-8531f.up.railway.app,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://web-production-8531f.up.railway.app
```

#### Step 4: Railway Auto-Deploys
- Railway automatically detects the push to GitHub
- Builds and deploys your application
- Your app will be live at: `https://web-production-8531f.up.railway.app`

#### Step 5: Run Migrations
1. Go to your service → **"Deployments"** tab
2. Click on the latest deployment
3. Click **"Shell"** tab
4. Run:
   ```bash
   python manage.py migrate
   ```

#### Step 6: Create Superuser
In the same shell:
```bash
python manage.py createsuperuser
```

---

### Method 2: Railway CLI (If You Install CLI)

#### Install Railway CLI

**Option A: Download Binary**
1. Go to https://railway.app/cli
2. Download Railway CLI for Windows
3. Extract and add to PATH

**Option B: Using npm (if you have Node.js)**
```bash
npm install -g @railway/cli
```

**Option C: Using Scoop (if installed)**
```bash
scoop install railway
```

#### After Installing CLI:

```powershell
# Set token
$env:RAILWAY_TOKEN="a8894331-04c6-4e82-9b65-dcd79c79c821"

# Login
railway login

# Link to project
railway link

# Set environment variables
railway variables set SECRET_KEY="-i`$kaay-4nd-k6xp58(h9l)gup@!=4hnl!-am582lz0nbl(s*s"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="web-production-8531f.up.railway.app,127.0.0.1,localhost"
railway variables set CSRF_TRUSTED_ORIGINS="https://web-production-8531f.up.railway.app"

# Run migrations
railway run python manage.py migrate

# Collect static files
railway run python manage.py collectstatic --noinput

# Deploy
railway up
```

---

## ✅ What's Already Done

1. ✅ **Settings Updated**: `ALLOWED_HOSTS` includes Railway domain
2. ✅ **Code Pushed**: All changes committed to GitHub
3. ✅ **Configuration Ready**: All Railway config files in place
4. ✅ **Environment Variables**: Documented and ready to set

---

## 🌐 Your Railway URL

**Public URL**: `https://web-production-8531f.up.railway.app`

### Available Endpoints:
- **Home**: https://web-production-8531f.up.railway.app/
- **API Docs**: https://web-production-8531f.up.railway.app/api/docs/
- **Admin**: https://web-production-8531f.up.railway.app/admin/
- **Patient Registration**: https://web-production-8531f.up.railway.app/access/patient/

---

## 🔍 Verification Steps

After deployment:

1. **Visit Home Page**: https://web-production-8531f.up.railway.app/
   - Should load without `DisallowedHost` error
   - Static files should load correctly

2. **Test Registration**: 
   - Go to https://web-production-8531f.up.railway.app/access/patient/
   - Register a new patient
   - Should redirect to login or appointments

3. **Test Login**:
   - Login with registered account
   - Should access appointments dashboard

4. **Test Admin**:
   - Go to https://web-production-8531f.up.railway.app/admin/
   - Login with superuser account
   - Should access Django admin

---

## 🐛 Troubleshooting

### If "DisallowedHost" Error:
1. Verify `ALLOWED_HOSTS` environment variable is set in Railway
2. Check domain matches exactly: `web-production-8531f.up.railway.app`
3. Redeploy after setting variables

### If Build Fails:
1. Check Railway build logs
2. Verify `runtime.txt` has `python-3.10.13`
3. Check `requirements.txt` is correct

### If Database Errors:
1. Verify PostgreSQL service is running
2. Check `DATABASE_URL` is set (automatic when PostgreSQL is added)
3. Run migrations in Railway shell

---

## 📝 Summary

**Current Status:**
- ✅ Code ready and pushed to GitHub
- ✅ Settings configured for Railway
- ✅ Environment variables documented
- ⏳ **Next**: Set variables in Railway Dashboard and deploy

**Recommended Action:**
Use **Method 1 (Railway Dashboard)** - it's the easiest and doesn't require CLI installation.

---

**Your project is ready! Just set the environment variables in Railway Dashboard and it will auto-deploy!** 🚀

