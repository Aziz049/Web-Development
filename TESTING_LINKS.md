# 🧪 Testing Links & Quick Start Guide

## 🚀 Start the Server

First, make sure the server is running:

```bash
python manage.py runserver
```

The server will start at: **http://localhost:8000**

---

## 📋 Testing Links

### 🌐 Main Application Pages

1. **Home Page**
   ```
   http://localhost:8000/
   ```

2. **Access/Registration Entry Point**
   ```
   http://localhost:8000/access/
   ```

3. **Patient Registration**
   ```
   http://localhost:8000/access/patient/
   ```

4. **Staff Authorization**
   ```
   http://localhost:8000/access/staff/authorize/
   ```

5. **Login Page**
   ```
   http://localhost:8000/login/
   ```

6. **Doctors List**
   ```
   http://localhost:8000/doctors/
   ```

7. **Appointments Dashboard**
   ```
   http://localhost:8000/appointments/
   ```

8. **Django Admin Panel**
   ```
   http://localhost:8000/admin/
   ```

---

## 📚 API Documentation Links

### Swagger UI (Interactive API Testing)
```
http://localhost:8000/api/docs/
```
**Features:**
- Interactive API documentation
- Test endpoints directly in browser
- Authorize with JWT tokens
- See request/response examples

### ReDoc (Alternative Documentation)
```
http://localhost:8000/api/redoc/
```
**Features:**
- Clean, readable API documentation
- Better for reading (less interactive)

### OpenAPI Schema (Download)
```
http://localhost:8000/api/schema/
```
**Features:**
- Download OpenAPI 3.0 schema
- Import into Postman, Insomnia, etc.

---

## 🔐 API Endpoints for Testing

### Authentication Endpoints

**1. Login (Get JWT Tokens)**
```
POST http://localhost:8000/api/auth/jwt/create/
Content-Type: application/json

{
  "email": "patient@example.com",
  "password": "SecurePass123"
}
```

**2. Register Patient (with Auto-Login)**
```
POST http://localhost:8000/api/auth/register/patient/
Content-Type: application/json

{
  "email": "newpatient@example.com",
  "username": "newpatient123",
  "password": "SecurePass123",
  "password2": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+96512345678",
  "date_of_birth": "1990-05-15",
  "gender": "M",
  "consent_treatment": true
}
```

**3. Register Staff**
```
POST http://localhost:8000/api/auth/register/staff/
Content-Type: application/json

{
  "email": "doctor@apexdental.com",
  "username": "doctor123",
  "password": "SecurePass123456",
  "password2": "SecurePass123456",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone_number": "+96512345678",
  "employee_id": "DOC001",
  "role_title": "Orthodontist",
  "department": "Dental",
  "specialization": "Orthodontics"
}
```

### Appointment Endpoints

**4. List Appointments**
```
GET http://localhost:8000/api/appointments/
Authorization: Bearer <your_access_token>
```

**5. Book Appointment**
```
POST http://localhost:8000/api/appointments/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "doctor_id": 2,
  "branch_id": 1,
  "appointment_date": "2024-12-20",
  "appointment_time": "10:00:00",
  "reason": "Regular checkup"
}
```

**6. Get Appointment History**
```
GET http://localhost:8000/api/appointments/history/
Authorization: Bearer <your_access_token>
```

**7. Get Current User Profile**
```
GET http://localhost:8000/api/users/me/
Authorization: Bearer <your_access_token>
```

---

## 🧪 Quick Testing Steps

### Option 1: Using Swagger UI (Easiest)

1. **Open Swagger UI**
   ```
   http://localhost:8000/api/docs/
   ```

2. **Login First**
   - Find `POST /api/auth/jwt/create/`
   - Click "Try it out"
   - Enter email and password
   - Click "Execute"
   - Copy the `access` token from response

3. **Authorize**
   - Click the green "Authorize" button at top
   - Paste your access token
   - Click "Authorize"
   - Click "Close"

4. **Test Endpoints**
   - All endpoints are now authorized
   - Click any endpoint → "Try it out" → Fill data → "Execute"

### Option 2: Using Postman

1. **Import Collection**
   - Open Postman
   - Click "Import"
   - Select `postman_collection.json` from project root

2. **Set Base URL**
   - Collection variables → `base_url` = `http://localhost:8000`

3. **Login**
   - Run "Login - Get JWT Tokens"
   - Tokens automatically saved to variables

4. **Test Endpoints**
   - All requests use saved tokens automatically

### Option 3: Using cURL

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "patient@example.com", "password": "SecurePass123"}'

# 2. Save the access token from response, then:
curl -X GET http://localhost:8000/api/appointments/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

## 🎯 Complete Test Workflow

### Step 1: Create Test Data (Optional)
```bash
python setup_db.py
```
This creates sample users:
- Admin: `admin@clinic.com` / `admin123`
- Doctor: `dr.smith@clinic.com` / `doctor123`
- Patient: `patient@example.com` / `patient123`

### Step 2: Test Patient Registration
1. Go to: http://localhost:8000/access/
2. Click "Patient"
3. Fill registration form
4. Submit → Auto-logged in with JWT tokens

### Step 3: Test API with Swagger
1. Go to: http://localhost:8000/api/docs/
2. Login to get token
3. Authorize with token
4. Test booking appointment
5. Test viewing appointments

### Step 4: Test Admin Panel
1. Go to: http://localhost:8000/admin/
2. Login as admin
3. View appointments with filters
4. Approve staff accounts

---

## 📝 Sample Test Credentials

If you ran `setup_db.py`:

**Admin:**
- Email: `admin@clinic.com`
- Password: `admin123`

**Doctor:**
- Email: `dr.smith@clinic.com`
- Password: `doctor123`

**Patient:**
- Email: `patient@example.com`
- Password: `patient123`

---

## 🔍 Quick Links Summary

| Purpose | Link |
|---------|------|
| **Swagger UI** (Best for API testing) | http://localhost:8000/api/docs/ |
| **ReDoc** (Readable docs) | http://localhost:8000/api/redoc/ |
| **Home Page** | http://localhost:8000/ |
| **Patient Registration** | http://localhost:8000/access/patient/ |
| **Login** | http://localhost:8000/login/ |
| **Appointments** | http://localhost:8000/appointments/ |
| **Admin Panel** | http://localhost:8000/admin/ |

---

## ✅ Recommended Testing Order

1. **Start Server**: `python manage.py runserver`
2. **Open Swagger**: http://localhost:8000/api/docs/
3. **Login**: Get JWT tokens
4. **Authorize**: Add token to Swagger
5. **Test Endpoints**: Try booking, listing, etc.
6. **Test Frontend**: Visit http://localhost:8000/access/
7. **Test Admin**: Visit http://localhost:8000/admin/

---

**Happy Testing!** 🚀


