# Apex Dental Care - Complete API Documentation

## 🔐 Authentication Flow

### JWT Token Authentication

All protected endpoints require JWT authentication. The flow is:

1. **Login** → `POST /api/auth/jwt/create/`
2. **Receive tokens** → `access` (1 hour) and `refresh` (1 day)
3. **Use access token** → Include in `Authorization: Bearer <access_token>` header
4. **Refresh token** → Use `refresh` token to get new `access` token when expired

---

## 📋 API Endpoints

### 1. Authentication Endpoints

#### Login (Get JWT Tokens)
```http
POST /api/auth/jwt/create/
Content-Type: application/json

{
  "email": "patient@example.com",
  "password": "SecurePass123"
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Refresh Token
```http
POST /api/auth/jwt/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 2. Registration Endpoints

#### Patient Registration (with Auto-Login)
```http
POST /api/auth/register/patient/
Content-Type: application/json

{
  "email": "patient@example.com",
  "username": "patient123",
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

**Response (201):**
```json
{
  "success": true,
  "message": "Registration successful! Your Patient ID is: PAT-001",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "patient@example.com",
    "username": "patient123",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "PATIENT"
  },
  "patient_id": "PAT-001"
}
```

**Error Response (400):**
```json
{
  "success": false,
  "errors": {
    "email": "This email is already registered...",
    "password": "Password must contain both letters and numbers."
  },
  "error": "Please correct the errors below and try again."
}
```

#### Staff Registration (Requires Admin Approval)
```http
POST /api/auth/register/staff/
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
  "specialization": "Orthodontics",
  "license_number": "LIC123456"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Registration submitted successfully. Your account is pending admin approval.",
  "employee_id": "DOC001"
}
```

---

### 3. Appointment Endpoints

#### List Appointments (Role-Based)
```http
GET /api/appointments/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `status` - Filter by status (UPCOMING, ATTENDED, MISSED, CANCELLED, COMPLETED)
- `date` - Filter by date (YYYY-MM-DD)
- `search` - Search by patient/doctor email, reason, notes
- `ordering` - Order by field (e.g., `-appointment_date`)

**Response (200):**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "patient": {
        "id": 1,
        "email": "patient@example.com",
        "first_name": "John",
        "last_name": "Doe"
      },
      "doctor": {
        "id": 2,
        "email": "doctor@apexdental.com",
        "first_name": "Jane",
        "last_name": "Smith"
      },
      "branch": {
        "id": 1,
        "name": "Main Clinic - Kuwait City"
      },
      "appointment_date": "2024-12-20",
      "appointment_time": "10:00:00",
      "status": "UPCOMING",
      "reason": "Regular checkup",
      "notes": null,
      "is_past": false,
      "created_at": "2024-12-15T10:00:00Z",
      "updated_at": "2024-12-15T10:00:00Z"
    }
  ]
}
```

**Role-Based Access:**
- **Patient**: Sees only their own appointments
- **Staff/Doctor**: Sees only their assigned appointments
- **Admin**: Sees all appointments

#### Book Appointment (Patient Only)
```http
POST /api/appointments/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "doctor_id": 2,
  "branch_id": 1,
  "appointment_date": "2024-12-20",
  "appointment_time": "10:00:00",
  "reason": "Regular checkup"
}
```

**Response (201):**
```json
{
  "id": 1,
  "patient": {...},
  "doctor": {...},
  "branch": {...},
  "appointment_date": "2024-12-20",
  "appointment_time": "10:00:00",
  "status": "UPCOMING",
  "reason": "Regular checkup",
  "notes": null,
  "is_past": false,
  "created_at": "2024-12-15T10:00:00Z",
  "updated_at": "2024-12-15T10:00:00Z"
}
```

**Error Response (400):**
```json
{
  "appointment_date": ["Appointment date cannot be in the past."],
  "non_field_errors": ["This time slot is not available. Please choose another time."]
}
```

#### Update Appointment Status (Doctor/Admin)
```http
PATCH /api/appointments/{id}/update_status/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "ATTENDED"
}
```

**Response (200):**
```json
{
  "id": 1,
  "status": "ATTENDED",
  ...
}
```

**Available Statuses:**
- `UPCOMING` - Future appointment
- `ATTENDED` - Patient attended
- `MISSED` - Patient did not attend
- `CANCELLED` - Appointment cancelled
- `COMPLETED` - Legacy status (backward compatibility)

#### Get Appointment History
```http
GET /api/appointments/history/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `status` - Filter by status

**Response (200):**
```json
{
  "upcoming": [
    {
      "id": 1,
      "appointment_date": "2024-12-20",
      "status": "UPCOMING",
      ...
    }
  ],
  "past": [
    {
      "id": 2,
      "appointment_date": "2024-12-10",
      "status": "ATTENDED",
      ...
    }
  ],
  "all": [...]
}
```

#### Get My Appointments
```http
GET /api/appointments/my_appointments/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "appointment_date": "2024-12-20",
    "status": "UPCOMING",
    ...
  }
]
```

#### Get Upcoming Appointments
```http
GET /api/appointments/upcoming/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "appointment_date": "2024-12-20",
    "status": "UPCOMING",
    ...
  }
]
```

#### Cancel Appointment (Patient Only)
```http
POST /api/appointments/{id}/cancel/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "status": "CANCELLED",
  ...
}
```

#### Mark Appointment as Attended (Doctor Only)
```http
POST /api/appointments/{id}/mark_attended/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "status": "ATTENDED",
  ...
}
```

#### Mark Appointment as Missed (Doctor Only)
```http
POST /api/appointments/{id}/mark_missed/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "status": "MISSED",
  ...
}
```

---

### 4. User & Profile Endpoints

#### Get Current User Profile
```http
GET /api/users/me/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "email": "patient@example.com",
  "username": "patient123",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "PATIENT",
  "patient_profile": {
    "patient_id": "PAT-001",
    "date_of_birth": "1990-05-15",
    "gender": "M"
  }
}
```

#### List Doctors
```http
GET /api/doctors/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "user": {
      "id": 2,
      "email": "doctor@apexdental.com",
      "first_name": "Jane",
      "last_name": "Smith"
    },
    "branch": {
      "id": 1,
      "name": "Main Clinic - Kuwait City"
    },
    "specialization": "Orthodontist",
    "years_of_experience": 12,
    "consultation_fee": 50.00,
    "is_available": true
  }
]
```

#### List Branches
```http
GET /api/branches/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Main Clinic - Kuwait City",
    "address": "Khalid Ibn Al Waleed St, Kuwait City",
    "phone": "22251515",
    "email": "info@apexdental.com",
    "is_active": true
  }
]
```

---

### 5. Visit History Endpoints (MongoDB)

#### List Visit History
```http
GET /api/visit-history/
Authorization: Bearer <access_token>
```

**Role-Based Access:**
- **Patient**: Sees only their own visit history
- **Doctor**: Sees visit history for their patients
- **Admin**: Sees all visit history

**Response (200):**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "appointment_id": 1,
    "patient_id": 1,
    "doctor_id": 2,
    "visit_date": "2024-12-10T10:00:00Z",
    "notes": "Regular checkup completed",
    "prescription": "Fluoride treatment recommended",
    "created_at": "2024-12-10T10:30:00Z"
  }
]
```

#### Add Visit History (Doctor Only)
```http
POST /api/appointments/{id}/add_visit_history/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "notes": "Regular checkup completed",
  "prescription": "Fluoride treatment recommended"
}
```

**Response (201):**
```json
{
  "message": "Visit history added successfully.",
  "visit_history_id": "507f1f77bcf86cd799439011"
}
```

---

## 🔒 Role-Based Permissions

### Patient Permissions
- ✅ Register account
- ✅ Login
- ✅ View own appointments
- ✅ Book appointments (future dates only)
- ✅ Cancel own appointments
- ✅ View own visit history
- ❌ Cannot update appointment status
- ❌ Cannot view other patients' data

### Staff/Doctor Permissions
- ✅ Login (after admin approval)
- ✅ View assigned appointments
- ✅ Update appointment status
- ✅ Mark appointments as attended/missed
- ✅ Add visit history for completed appointments
- ✅ Manage own schedule
- ❌ Cannot book appointments for patients
- ❌ Cannot view other doctors' appointments

### Admin Permissions
- ✅ Full access to all endpoints
- ✅ View all appointments
- ✅ Approve/reject staff accounts
- ✅ Access reports and analytics
- ✅ Manage all users and profiles

---

## 📝 Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message for this field"],
  "non_field_errors": ["General validation errors"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "error": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "An unexpected error occurred. Please try again later."
}
```

---

## 🧪 Testing with cURL

### Login
```bash
curl -X POST http://localhost:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "patient@example.com", "password": "SecurePass123"}'
```

### Book Appointment
```bash
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": 2,
    "branch_id": 1,
    "appointment_date": "2024-12-20",
    "appointment_time": "10:00:00",
    "reason": "Regular checkup"
  }'
```

### List Appointments
```bash
curl -X GET http://localhost:8000/api/appointments/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 📚 API Documentation (Swagger/OpenAPI)

### Access Swagger UI
```
http://localhost:8000/api/docs/
```

### Access ReDoc
```
http://localhost:8000/api/redoc/
```

### Download OpenAPI Schema
```
http://localhost:8000/api/schema/
```

---

## ✅ Validation Rules

### Password Requirements
- Minimum 8 characters (patients)
- Minimum 12 characters (staff)
- Must contain at least one letter
- Must contain at least one number

### Email Requirements
- Valid email format
- Must be unique
- Staff must use clinic email domain (@apexdental.com)

### Appointment Requirements
- Date cannot be in the past
- Time cannot be in the past (for today)
- Time slot must be available
- Doctor must belong to selected branch

---

**For complete API documentation with interactive testing, visit:**
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`


