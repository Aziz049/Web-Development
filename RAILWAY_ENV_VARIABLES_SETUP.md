# Railway Environment Variables Setup Guide

## 📋 Required Environment Variables

Set these in Railway Dashboard → Your Service → Variables:

### 1. Database Configuration
```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
```
**Note**: Railway automatically provides this when you add a PostgreSQL database service. You don't need to set it manually.

### 2. Django Secret Key
```bash
SECRET_KEY=-i$kaay-4nd-k6xp58(h9l)gup@!=4hnl!-am582lz0nbl(s*s
```
**Important**: Generate a new secret key for production! Use:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Debug Mode
```bash
DEBUG=False
```
**Important**: Always set to `False` in production for security.

### 4. Allowed Hosts
```bash
ALLOWED_HOSTS=web-production-8531f.up.railway.app,127.0.0.1,localhost
```
**Note**: Replace `web-production-8531f.up.railway.app` with your actual Railway domain.

### 5. CSRF Trusted Origins
```bash
CSRF_TRUSTED_ORIGINS=https://web-production-8531f.up.railway.app
```
**Note**: Replace with your actual Railway domain. Must use `https://` protocol.

### 6. CORS Allowed Origins (Optional)
```bash
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```
**Note**: Only needed if you have a separate frontend application.

---

## 🚀 How to Set Environment Variables in Railway

### Method 1: Railway Dashboard (Recommended)

1. Go to https://railway.app
2. Select your project
3. Click on your **service** (Django app)
4. Go to **"Variables"** tab
5. Click **"+ New Variable"**
6. Enter variable name and value
7. Click **"Add"**
8. Railway will automatically redeploy with new variables

### Method 2: Railway CLI

```bash
# Set individual variables
railway variables set SECRET_KEY="your-secret-key"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="web-production-8531f.up.railway.app,127.0.0.1,localhost"
railway variables set CSRF_TRUSTED_ORIGINS="https://web-production-8531f.up.railway.app"

# View all variables
railway variables

# Delete a variable
railway variables delete VARIABLE_NAME
```

---

## ✅ Verification Checklist

After setting environment variables:

- [ ] `DATABASE_URL` is set (automatically by Railway when PostgreSQL is added)
- [ ] `SECRET_KEY` is set with a secure random value
- [ ] `DEBUG=False` is set
- [ ] `ALLOWED_HOSTS` includes your Railway domain
- [ ] `CSRF_TRUSTED_ORIGINS` includes your Railway domain with `https://`
- [ ] Railway has redeployed successfully
- [ ] Website loads without `DisallowedHost` errors
- [ ] Database connections work (run migrations)

---

## 🔧 Troubleshooting

### Issue: "DisallowedHost" Error
**Solution**: 
- Verify `ALLOWED_HOSTS` includes your exact Railway domain
- Check domain matches exactly (case-sensitive)
- Redeploy after setting variable

### Issue: Database Connection Failed
**Solution**:
- Verify PostgreSQL service is running in Railway
- Check `DATABASE_URL` is set (Railway sets this automatically)
- Verify database credentials are correct

### Issue: CSRF Token Errors
**Solution**:
- Verify `CSRF_TRUSTED_ORIGINS` includes your Railway domain
- Must use `https://` protocol
- Domain must match exactly

---

## 📝 Example Complete Setup

```bash
# In Railway Dashboard → Variables:

DATABASE_URL=postgresql://postgres:password@containers-us-west-123.railway.app:5432/railway
SECRET_KEY=django-insecure-your-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=web-production-8531f.up.railway.app,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://web-production-8531f.up.railway.app
```

---

**✅ Your project is now configured to use `dj-database-url` for Railway PostgreSQL connection!**


