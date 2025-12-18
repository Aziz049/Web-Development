# Railway Deployment Guide - Apex Dental Care

## 🚂 Deploy to Railway

Railway is a modern platform that makes deployment simple. This guide will help you deploy the Apex Dental Care Appointment Manager to Railway.

---

## 📋 Prerequisites

1. **Railway Account**: Sign up at https://railway.app (free tier available)
2. **GitHub Account**: Your code should be on GitHub
3. **PostgreSQL**: Railway provides PostgreSQL automatically

---

## 🚀 Quick Deployment Steps

### Step 1: Create Railway Project

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Connect your GitHub account
5. Select your repository: `Web-Development` (or your repo name)

### Step 2: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically:
   - Create PostgreSQL database
   - Set `DATABASE_URL` environment variable
   - Connect it to your service

### Step 3: Configure Environment Variables

In your Railway service, go to **"Variables"** tab and add:

#### Required Variables

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.up.railway.app,localhost,127.0.0.1
```

#### Optional Variables (for MongoDB visit history)

```bash
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=clinic_appointment
MONGODB_COLLECTION_NAME=visit_history
```

#### Optional Variables (for staff registration)

```bash
STAFF_EMPLOYEE_ID=DOC001
STAFF_CLINIC_CODE=CLINIC2024
CLINIC_EMAIL_DOMAIN=@apexdental.com
```

#### CORS & CSRF (if needed)

```bash
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CSRF_TRUSTED_ORIGINS=https://your-app-name.up.railway.app
```

### Step 4: Generate Secret Key

Run this locally to generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as `SECRET_KEY` in Railway variables.

### Step 5: Configure Build Settings

Railway will automatically detect:
- **Python** (from `runtime.txt`)
- **Dependencies** (from `requirements.txt`)
- **Start Command** (from `Procfile`)

No additional configuration needed!

### Step 6: Deploy

Railway will automatically:
1. Build your application
2. Install dependencies
3. Run migrations (if configured)
4. Start the server with Gunicorn

**Your app will be live at**: `https://your-app-name.up.railway.app`

---

## 🔧 Railway-Specific Configuration

### Automatic Database Connection

Railway automatically provides `DATABASE_URL` when you add PostgreSQL. The project is configured to use it automatically via `dj-database-url`.

**No manual database configuration needed!**

### Static Files

WhiteNoise is configured to serve static files. Railway will:
1. Run `collectstatic` automatically during build
2. Serve static files via WhiteNoise middleware

### Port Configuration

Railway provides `$PORT` environment variable. The `Procfile` is configured to use it:
```
web: gunicorn clinic_appointment.wsgi --bind 0.0.0.0:$PORT
```

---

## 📝 Post-Deployment Steps

### 1. Run Migrations

After first deployment, run migrations:

1. Go to Railway dashboard
2. Click on your service
3. Go to **"Deployments"** tab
4. Click on the latest deployment
5. Open **"Shell"** tab
6. Run:
   ```bash
   python manage.py migrate
   ```

### 2. Create Superuser

In the same shell:
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 3. Verify Deployment

Visit your Railway URL:
- **Home**: `https://your-app-name.up.railway.app/`
- **API Docs**: `https://your-app-name.up.railway.app/api/docs/`
- **Admin**: `https://your-app-name.up.railway.app/admin/`

---

## 🔍 Troubleshooting

### Database Connection Issues

**Problem**: Database connection fails

**Solution**:
1. Verify PostgreSQL service is running in Railway
2. Check `DATABASE_URL` is set automatically (Railway does this)
3. Verify migrations ran: Check deployment logs

### Static Files Not Loading

**Problem**: CSS/JS files return 404

**Solution**:
1. Check deployment logs for `collectstatic` output
2. Verify `STATIC_ROOT` is set correctly
3. Ensure WhiteNoise middleware is enabled (it is)

### CORS Errors

**Problem**: Frontend can't access API

**Solution**:
1. Add your frontend domain to `CORS_ALLOWED_ORIGINS`
2. Add Railway domain to `CSRF_TRUSTED_ORIGINS`
3. Set `CORS_ALLOW_CREDENTIALS=True` (already set)

### 500 Internal Server Error

**Problem**: App crashes on Railway

**Solution**:
1. Check Railway deployment logs
2. Verify all environment variables are set
3. Ensure `DEBUG=False` in production
4. Check database migrations completed

---

## 📊 Environment Variables Reference

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Generated key |
| `DEBUG` | Debug mode | `False` (production) |
| `ALLOWED_HOSTS` | Allowed domains | `your-app.up.railway.app` |

### Automatic (Railway Provides)

| Variable | Description | Auto-set? |
|----------|-------------|-----------|
| `DATABASE_URL` | PostgreSQL connection | ✅ Yes |
| `PORT` | Server port | ✅ Yes |
| `RAILWAY_ENVIRONMENT` | Environment name | ✅ Yes |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection | None |
| `CORS_ALLOWED_ORIGINS` | CORS origins | Railway domains |
| `CSRF_TRUSTED_ORIGINS` | CSRF trusted origins | Railway domains |

---

## 🔄 Continuous Deployment

Railway automatically deploys when you push to your connected GitHub branch.

**Workflow**:
1. Push code to GitHub
2. Railway detects changes
3. Builds and deploys automatically
4. Your app updates live

---

## 📈 Monitoring

### View Logs

1. Go to Railway dashboard
2. Click your service
3. Click **"Deployments"**
4. Click latest deployment
5. View **"Logs"** tab

### View Metrics

Railway provides:
- Request metrics
- Error rates
- Response times
- Resource usage

---

## 🎯 Production Checklist

- [ ] PostgreSQL database added
- [ ] `SECRET_KEY` set (strong, random)
- [ ] `DEBUG=False` set
- [ ] `ALLOWED_HOSTS` includes Railway domain
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Static files collected
- [ ] CORS configured (if using frontend)
- [ ] CSRF trusted origins set
- [ ] Test registration flow
- [ ] Test login flow
- [ ] Test appointment booking
- [ ] Test admin panel

---

## 🌐 Your Live URLs

After deployment, your app will be available at:

- **Home**: `https://your-app-name.up.railway.app/`
- **API Docs**: `https://your-app-name.up.railway.app/api/docs/`
- **ReDoc**: `https://your-app-name.up.railway.app/api/redoc/`
- **Admin**: `https://your-app-name.up.railway.app/admin/`

---

## 💡 Tips

1. **Free Tier**: Railway free tier is generous for development/testing
2. **Auto-Deploy**: Every push to main branch auto-deploys
3. **Database Backups**: Railway provides automatic PostgreSQL backups
4. **Custom Domain**: You can add your own domain in Railway settings
5. **Environment Variables**: Keep secrets in Railway, never commit to Git

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Django on Railway](https://docs.railway.app/guides/django)
- [PostgreSQL on Railway](https://docs.railway.app/databases/postgresql)

---

**Ready to deploy!** 🚀


