# Railway Environment Variables Reference

## Required Variables

Set these in Railway dashboard → Your Service → Variables:

### 1. SECRET_KEY
```bash
SECRET_KEY=your-generated-secret-key-here
```

**Generate:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. DEBUG
```bash
DEBUG=False
```

### 3. ALLOWED_HOSTS
```bash
ALLOWED_HOSTS=your-app-name.up.railway.app,localhost,127.0.0.1
```

Replace `your-app-name` with your actual Railway app name.

---

## Automatic Variables (Railway Provides)

These are set automatically by Railway - **DO NOT SET MANUALLY**:

- ✅ `DATABASE_URL` - PostgreSQL connection string (auto-set when you add PostgreSQL)
- ✅ `PORT` - Server port (auto-set by Railway)
- ✅ `RAILWAY_ENVIRONMENT` - Environment name (auto-set)

---

## Optional Variables

### MongoDB (for Visit History)
```bash
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=clinic_appointment
MONGODB_COLLECTION_NAME=visit_history
```

### Staff Registration
```bash
STAFF_EMPLOYEE_ID=DOC001
STAFF_CLINIC_CODE=CLINIC2024
CLINIC_EMAIL_DOMAIN=@apexdental.com
```

### CORS (if using separate frontend)
```bash
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CSRF_TRUSTED_ORIGINS=https://your-app-name.up.railway.app
```

### Security (Production)
```bash
SECURE_SSL_REDIRECT=True
```

---

## How to Set in Railway

1. Go to Railway dashboard
2. Click your service
3. Click **"Variables"** tab
4. Click **"+ New Variable"**
5. Enter variable name and value
6. Click **"Add"**

---

## Verification

After setting variables, Railway will:
1. Automatically redeploy
2. Use new variables in next deployment
3. Show in deployment logs if there are issues

---

**Note**: Never commit secrets to Git! Always use Railway environment variables.

