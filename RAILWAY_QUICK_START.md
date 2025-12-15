# Railway Quick Start - 5 Minutes

## 🚀 Deploy in 5 Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Configure for Railway deployment"
git push origin main
```

### 2. Create Railway Project
- Go to https://railway.app
- Click **"New Project"**
- Select **"Deploy from GitHub repo"**
- Choose your repository

### 3. Add PostgreSQL
- In Railway project, click **"+ New"**
- Select **"Database"** → **"Add PostgreSQL"**
- Railway sets `DATABASE_URL` automatically ✅

### 4. Set Environment Variables
In Railway service → **Variables** tab:

```bash
SECRET_KEY=<generate-with-command-below>
DEBUG=False
ALLOWED_HOSTS=your-app-name.up.railway.app
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Deploy!
Railway auto-deploys. Wait 2-3 minutes, then:

1. Click **"Deployments"** → Latest deployment → **"Shell"**
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

**Done!** Your app is live at: `https://your-app-name.up.railway.app`

---

## ✅ Verify Deployment

- **Home**: `https://your-app-name.up.railway.app/`
- **API Docs**: `https://your-app-name.up.railway.app/api/docs/`
- **Admin**: `https://your-app-name.up.railway.app/admin/`

---

**Full Guide**: See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

