# Railway Domain Setup Guide

## 🔍 Finding Your Railway Domain

### Step 1: Access Railway Dashboard
1. Go to https://railway.app
2. Log in to your account
3. Select your project

### Step 2: Find Your Domain
1. Click on your **service** (Django app)
2. Go to **"Settings"** tab
3. Scroll to **"Domains"** section
4. You'll see your Railway domain, for example:
   - `web-production-8531f.up.railway.app`
   - `your-app-name.up.railway.app`

### Step 3: Copy Your Domain
Copy the full domain (e.g., `web-production-8531f.up.railway.app`)

---

## ⚙️ Setting ALLOWED_HOSTS in Railway

### Option 1: Specific Domain (Recommended for Production)

1. Go to Railway dashboard → Your Service → **"Variables"** tab
2. Click **"+ New Variable"**
3. Set:
   - **Name**: `ALLOWED_HOSTS`
   - **Value**: `web-production-8531f.up.railway.app,127.0.0.1,localhost`
   - Replace `web-production-8531f.up.railway.app` with your actual domain

4. Click **"Add"**

### Option 2: Wildcard (Convenient but Less Secure)

If you want to allow any Railway subdomain:

1. Set **Name**: `ALLOWED_HOSTS`
2. Set **Value**: `*.up.railway.app,*.railway.app,127.0.0.1,localhost`

**Note**: Wildcards are convenient but less secure. Use specific domain for production.

---

## 🔧 Complete Environment Variables Setup

### Required Variables:

```bash
SECRET_KEY=<your-secret-key>
DEBUG=False
ALLOWED_HOSTS=web-production-8531f.up.railway.app,127.0.0.1,localhost
```

### Optional Variables:

```bash
CSRF_TRUSTED_ORIGINS=https://web-production-8531f.up.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

---

## ✅ Verification

After setting `ALLOWED_HOSTS`:

1. **Redeploy** your service (Railway auto-redeploys on variable changes)
2. **Visit** your Railway URL: `https://web-production-8531f.up.railway.app`
3. **Check** that the site loads without `DisallowedHost` error

---

## 🐛 Troubleshooting

### Error: "DisallowedHost at /"
**Solution**: 
- Verify `ALLOWED_HOSTS` includes your Railway domain
- Check domain format (no `https://`, no trailing slash)
- Redeploy after setting variable

### Error: "Invalid HTTP_HOST header"
**Solution**:
- Ensure domain in `ALLOWED_HOSTS` matches exactly
- Check for typos in domain name
- Use wildcard if unsure: `*.up.railway.app`

### Site Still Not Loading
**Solution**:
1. Check Railway deployment logs
2. Verify `DEBUG=False` is set
3. Verify `SECRET_KEY` is set
4. Check Railway service is running

---

## 📝 Example Configuration

### For Production:
```bash
SECRET_KEY=django-insecure-...your-key...
DEBUG=False
ALLOWED_HOSTS=web-production-8531f.up.railway.app,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://web-production-8531f.up.railway.app
```

### For Local Development:
```bash
# .env file (local only)
SECRET_KEY=django-insecure-dev-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
# DATABASE_URL not needed (uses SQLite)
```

---

**Status**: ✅ Ready - Set `ALLOWED_HOSTS` in Railway with your domain


