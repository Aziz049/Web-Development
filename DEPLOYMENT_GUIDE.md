# Deployment Guide - Heroku

## 🚀 Heroku Deployment Steps

### Prerequisites
- Heroku account (free tier available)
- Git installed
- Heroku CLI installed

### 1. Install Heroku CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
# Or use package manager:
# Windows: choco install heroku-cli
# macOS: brew install heroku/brew/heroku
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Create Heroku App
```bash
heroku create apex-dental-appointment-manager
# Or use your preferred app name
```

### 4. Set Environment Variables
```bash
# Set Django secret key
heroku config:set SECRET_KEY="your-secret-key-here"

# Set debug mode (False for production)
heroku config:set DEBUG=False

# Set allowed hosts
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"

# Database (Heroku provides PostgreSQL automatically)
# MongoDB Atlas connection string
heroku config:set MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
heroku config:set MONGODB_DB_NAME="clinic_appointment"
heroku config:set MONGODB_COLLECTION_NAME="visit_history"

# Staff authorization (optional, for staff registration)
heroku config:set STAFF_EMPLOYEE_ID="DOC001"
heroku config:set STAFF_CLINIC_CODE="CLINIC2024"
heroku config:set CLINIC_EMAIL_DOMAIN="@apexdental.com"
```

### 5. Add PostgreSQL Add-on
```bash
heroku addons:create heroku-postgresql:mini
# Free tier: hobby-dev (for production, use paid tier)
```

### 6. Update settings.py for Production
The project already includes:
- `Procfile` - Gunicorn server configuration
- `runtime.txt` - Python version
- `whitenoise` - Static file serving
- `python-decouple` - Environment variable management

### 7. Run Migrations
```bash
heroku run python manage.py migrate
```

### 8. Create Superuser
```bash
heroku run python manage.py createsuperuser
```

### 9. Collect Static Files
```bash
heroku run python manage.py collectstatic --noinput
```

### 10. Deploy
```bash
# Add and commit changes
git add .
git commit -m "Prepare for Heroku deployment"

# Push to Heroku
git push heroku main
```

### 11. Open Your App
```bash
heroku open
```

---

## 📋 Environment Variables Checklist

### Required Variables
- `SECRET_KEY` - Django secret key (generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG` - Set to `False` for production
- `ALLOWED_HOSTS` - Your Heroku app domain
- `DATABASE_URL` - Automatically set by Heroku PostgreSQL add-on
- `MONGODB_URI` - MongoDB Atlas connection string (optional, for visit history)

### Optional Variables
- `STAFF_EMPLOYEE_ID` - For staff authorization
- `STAFF_CLINIC_CODE` - For staff authorization
- `CLINIC_EMAIL_DOMAIN` - For staff email validation
- `DEFAULT_FROM_EMAIL` - For email notifications

---

## 🔧 Configuration Files

### Procfile
```
web: gunicorn clinic_appointment.wsgi --log-file -
```

### runtime.txt
```
python-3.11.0
```

### requirements.txt
Already includes:
- `gunicorn` - WSGI server
- `whitenoise` - Static file serving
- `psycopg2-binary` - PostgreSQL adapter
- `python-decouple` - Environment variables

---

## 📊 Database Setup

### PostgreSQL (Heroku)
- Automatically provisioned with `heroku-postgresql` add-on
- Connection string in `DATABASE_URL` environment variable
- Django settings automatically use `DATABASE_URL` if available

### MongoDB Atlas (Optional)
1. Create account at https://www.mongodb.com/cloud/atlas
2. Create cluster (free tier available)
3. Get connection string
4. Set `MONGODB_URI` in Heroku config

---

## 🧪 Post-Deployment Testing

### 1. Test API Endpoints
```bash
# Test login
curl -X POST https://your-app.herokuapp.com/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Test appointments list
curl -X GET https://your-app.herokuapp.com/api/appointments/ \
  -H "Authorization: Bearer <access_token>"
```

### 2. Test Admin Panel
```
https://your-app.herokuapp.com/admin/
```

### 3. Test Swagger Documentation
```
https://your-app.herokuapp.com/api/docs/
```

---

## 🔍 Troubleshooting

### Static Files Not Loading
```bash
# Ensure WhiteNoise is configured in settings.py
# Run collectstatic
heroku run python manage.py collectstatic --noinput
```

### Database Connection Issues
```bash
# Check database URL
heroku config:get DATABASE_URL

# Run migrations
heroku run python manage.py migrate
```

### Application Errors
```bash
# View logs
heroku logs --tail

# Check specific error
heroku logs --tail | grep ERROR
```

---

## 📝 Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Set `ALLOWED_HOSTS` correctly
- [ ] Generate new `SECRET_KEY`
- [ ] Configure PostgreSQL database
- [ ] Run migrations
- [ ] Create superuser
- [ ] Collect static files
- [ ] Test all API endpoints
- [ ] Test admin panel
- [ ] Configure email (if needed)
- [ ] Set up MongoDB Atlas (if using visit history)
- [ ] Test registration flows
- [ ] Test appointment booking
- [ ] Verify role-based permissions

---

## 🌐 Live Demo URL

After deployment, your app will be available at:
```
https://your-app-name.herokuapp.com
```

**API Documentation:**
- Swagger UI: `https://your-app-name.herokuapp.com/api/docs/`
- ReDoc: `https://your-app-name.herokuapp.com/api/redoc/`

---

## 📚 Additional Resources

- [Heroku Django Deployment Guide](https://devcenter.heroku.com/articles/django-app-configuration)
- [Heroku PostgreSQL](https://devcenter.heroku.com/articles/heroku-postgresql)
- [WhiteNoise Documentation](https://whitenoise.readthedocs.io/)

