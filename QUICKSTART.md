# Quick Start Guide

## Fast Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Database
```bash
# Create PostgreSQL database (if not exists)
createdb clinic_appointment_db

# Or using psql
psql -U postgres -c "CREATE DATABASE clinic_appointment_db;"
```

### 3. Configure Environment (Optional)
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=clinic_appointment_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. (Optional) Create Sample Data
```bash
python setup_db.py
```

### 7. Run Server
```bash
python manage.py runserver
```

### 8. Access the Application
- **Frontend**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Root**: http://localhost:8000/api/

## Testing the API

### Using DRF Browsable API
1. Go to http://localhost:8000/api/
2. Click on any endpoint
3. Use the "Authentication" button to login with JWT tokens

### Using curl

**Register a patient:**
```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123",
    "password_retype": "testpass123",
    "role": "PATIENT"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

**Get doctors list (with token):**
```bash
curl -X GET http://localhost:8000/api/api/users/doctors/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Sample Users (if you ran setup_db.py)

- **Admin**: admin@clinic.com / admin123
- **Doctor**: dr.smith@clinic.com / doctor123
- **Patient**: patient@example.com / patient123

## Common Issues

### Database Connection Error
- Ensure PostgreSQL is running
- Check database credentials in `.env` or settings
- Verify database exists: `psql -l | grep clinic_appointment_db`

### Migration Errors
- Delete migration files (except `__init__.py`) and run `makemigrations` again
- Or reset database: `dropdb clinic_appointment_db && createdb clinic_appointment_db`

### Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### CORS Errors
- Check CORS settings in `settings.py`
- Ensure frontend URL is in `CORS_ALLOWED_ORIGINS`

## Next Steps

1. Explore the API using the browsable API interface
2. Test the frontend at http://localhost:8000
3. Create more users and appointments
4. Customize the admin panel
5. Deploy to production (see README.md)

