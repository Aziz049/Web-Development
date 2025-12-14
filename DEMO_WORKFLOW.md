# Complete Demo Workflow - Apex Dental Care

## 🎯 Demo Scenario

This document provides a step-by-step guide for demonstrating the complete appointment management workflow.

---

## 👤 Patient Registration & Booking Flow

### Step 1: Patient Registration
1. **Navigate to**: `http://localhost:8000/access/`
2. **Select**: "Patient"
3. **Fill Registration Form**:
   - Personal Information: First Name, Last Name, Date of Birth, Gender
   - Contact Details: Username, Email, Phone Number
   - Medical Info: (Optional) Medical conditions, allergies, etc.
   - Account Security: Password (min 8 chars, letters + numbers)
   - Consents: Check "I consent to treatment"
4. **Submit**: Click "Complete Registration"
5. **Result**: 
   - ✅ Patient account created
   - ✅ PatientProfile created with Patient ID
   - ✅ JWT tokens returned (auto-login)
   - ✅ Redirected to `/appointments/` dashboard
   - ✅ Welcome message displayed

### Step 2: Patient Views Doctors
1. **Navigate to**: `http://localhost:8000/doctors/`
2. **View**: List of available doctors with:
   - Name and specialization
   - Branch location
   - Availability status
   - Consultation fee

### Step 3: Patient Books Appointment
1. **Navigate to**: `http://localhost:8000/appointments/`
2. **Click**: "Book New Appointment"
3. **Fill Form**:
   - Doctor ID: Select from available doctors
   - Date: Future date (YYYY-MM-DD)
   - Time: Available time slot (HH:MM)
   - Reason: (Optional) Appointment reason
4. **Submit**: Click "Book"
5. **Result**:
   - ✅ Appointment created with status "UPCOMING"
   - ✅ Appointment appears in patient's appointment list
   - ✅ Time slot marked as unavailable

### Step 4: Patient Views Appointment History
1. **Navigate to**: `http://localhost:8000/appointments/`
2. **View**: 
   - Upcoming appointments (future dates)
   - Past appointments with status (ATTENDED, MISSED, CANCELLED)
   - Appointment details (date, time, doctor, status)

---

## 👨‍⚕️ Doctor/Staff Workflow

### Step 1: Staff Registration (Requires Authorization)
1. **Navigate to**: `http://localhost:8000/access/`
2. **Select**: "Staff"
3. **Authorization Gate**:
   - Enter Employee ID (e.g., "DOC001")
   - Enter Clinic Registration Code (from environment variables)
   - Complete CAPTCHA (if required after 2 failed attempts)
4. **Staff Registration Form**:
   - Identity: First Name, Last Name, Email (must be @apexdental.com)
   - Credentials: Username, Password (min 12 chars)
   - Professional Details: Role Title, Department, Specialization, License Number
5. **Submit**: Click "Complete Registration"
6. **Result**:
   - ✅ Staff account created (inactive)
   - ✅ StaffProfile created
   - ✅ Account pending admin approval

### Step 2: Admin Approves Staff
1. **Navigate to**: `http://localhost:8000/admin/`
2. **Login**: As superuser
3. **Go to**: Staff Profiles
4. **Filter**: Show only unapproved staff
5. **Select**: Staff account to approve
6. **Action**: Click "Approve selected staff accounts"
7. **Result**:
   - ✅ Staff account activated
   - ✅ Staff receives activation email
   - ✅ Staff can now log in

### Step 3: Doctor Logs In
1. **Navigate to**: `http://localhost:8000/login/`
2. **Enter**: Staff email and password
3. **Submit**: Login
4. **Result**:
   - ✅ JWT tokens received
   - ✅ Redirected to dashboard

### Step 4: Doctor Views Appointments
1. **Navigate to**: `http://localhost:8000/appointments/`
2. **View**: List of assigned appointments
3. **Filter**: By status, date, etc.

### Step 5: Doctor Updates Appointment Status
1. **Select**: An appointment
2. **Actions Available**:
   - Mark as Attended (for past appointments)
   - Mark as Missed (for past appointments)
   - Update Status (UPCOMING, ATTENDED, MISSED, CANCELLED)
3. **Result**: Appointment status updated

### Step 6: Doctor Adds Visit History
1. **Select**: A completed appointment
2. **Action**: Add Visit History
3. **Enter**:
   - Notes: "Regular checkup completed"
   - Prescription: "Fluoride treatment recommended"
4. **Submit**: Add Visit History
5. **Result**:
   - ✅ Visit history saved to MongoDB
   - ✅ Linked to appointment, patient, and doctor

---

## 🔐 API Testing Workflow

### Using Postman Collection

1. **Import Collection**: Import `postman_collection.json` into Postman
2. **Set Base URL**: Update `base_url` variable to your server URL
3. **Test Authentication**:
   - Run "Login - Get JWT Tokens"
   - Tokens automatically saved to collection variables
4. **Test Registration**:
   - Run "Register Patient (with Auto-Login)"
   - Tokens automatically saved
5. **Test Appointments**:
   - Run "Book Appointment" (requires patient token)
   - Run "List Appointments" (role-based results)
   - Run "Update Appointment Status" (requires doctor token)

### Using Swagger UI

1. **Navigate to**: `http://localhost:8000/api/docs/`
2. **Authorize**: Click "Authorize" button
3. **Enter Token**: Paste JWT access token
4. **Test Endpoints**: Use interactive API documentation

---

## 📊 Admin Panel Workflow

### Customized Admin Features

1. **Appointments Admin**:
   - **List Display**: ID, Patient Name, Doctor Name, Branch, Date, Time, Status, Past Indicator
   - **Filters**: Status, Date, Doctor, Branch
   - **Search**: Patient name, Doctor name, Reason, Notes, Branch name
   - **Date Hierarchy**: Navigate by appointment date

2. **Users Admin**:
   - **List Display**: Email, Username, Full Name, User Type, Active Status, Superuser Status
   - **Filters**: User Type, Active Status, Superuser Status, Date Joined
   - **Search**: Email, Username, First Name, Last Name, Phone Number

3. **Staff Approval**:
   - **List Display**: Employee ID, User, Role Title, Department, Email, Approval Status
   - **Filters**: Approval Status, Department, Role Title
   - **Actions**: Approve selected, Reject selected
   - **Auto-Email**: Activation email sent on approval

---

## 🧪 Complete Test Scenario

### Scenario: End-to-End Appointment Flow

1. **Patient Registration**
   ```
   POST /api/auth/register/patient/
   → Returns: access_token, refresh_token, patient_id
   ```

2. **Patient Logs In** (if not auto-logged in)
   ```
   POST /api/auth/jwt/create/
   → Returns: access_token, refresh_token
   ```

3. **Patient Views Doctors**
   ```
   GET /api/doctors/
   Authorization: Bearer <access_token>
   → Returns: List of available doctors
   ```

4. **Patient Books Appointment**
   ```
   POST /api/appointments/
   Authorization: Bearer <access_token>
   Body: {doctor_id, branch_id, appointment_date, appointment_time, reason}
   → Returns: Created appointment
   ```

5. **Patient Views Appointments**
   ```
   GET /api/appointments/my_appointments/
   Authorization: Bearer <access_token>
   → Returns: Patient's appointments
   ```

6. **Doctor Logs In**
   ```
   POST /api/auth/jwt/create/
   Body: {email: "doctor@apexdental.com", password: "..."}
   → Returns: access_token, refresh_token
   ```

7. **Doctor Views Appointments**
   ```
   GET /api/appointments/
   Authorization: Bearer <doctor_access_token>
   → Returns: Doctor's assigned appointments
   ```

8. **Doctor Updates Status**
   ```
   PATCH /api/appointments/{id}/update_status/
   Authorization: Bearer <doctor_access_token>
   Body: {status: "ATTENDED"}
   → Returns: Updated appointment
   ```

9. **Doctor Adds Visit History**
   ```
   POST /api/appointments/{id}/add_visit_history/
   Authorization: Bearer <doctor_access_token>
   Body: {notes: "...", prescription: "..."}
   → Returns: Visit history ID
   ```

10. **Patient Views Visit History**
    ```
    GET /api/visit-history/
    Authorization: Bearer <patient_access_token>
    → Returns: Patient's visit history
    ```

---

## ✅ Demo Checklist

### Patient Flow
- [ ] Patient registers successfully
- [ ] Patient receives Patient ID
- [ ] Patient auto-logged in (JWT tokens)
- [ ] Patient views doctors list
- [ ] Patient books appointment
- [ ] Patient views appointment history
- [ ] Patient can cancel appointment

### Staff Flow
- [ ] Staff completes authorization
- [ ] Staff registers (account inactive)
- [ ] Admin approves staff account
- [ ] Staff logs in successfully
- [ ] Staff views assigned appointments
- [ ] Staff updates appointment status
- [ ] Staff adds visit history

### Admin Flow
- [ ] Admin logs in
- [ ] Admin views all appointments
- [ ] Admin filters appointments (date, doctor, status)
- [ ] Admin searches appointments
- [ ] Admin approves staff accounts
- [ ] Admin views reports

### API Testing
- [ ] All endpoints accessible via Postman
- [ ] JWT authentication works
- [ ] Role-based permissions enforced
- [ ] Error handling works correctly
- [ ] Swagger documentation accessible

---

## 🎬 Presentation Tips

1. **Start with Patient Registration**: Show the complete onboarding experience
2. **Demonstrate Auto-Login**: Show JWT tokens returned and user redirected
3. **Show Role-Based Access**: Compare patient view vs doctor view
4. **Demonstrate Admin Panel**: Show filters, search, and approval workflow
5. **Test API Endpoints**: Use Swagger UI for interactive demonstration
6. **Show Error Handling**: Demonstrate validation errors and friendly messages
7. **MongoDB Integration**: Show visit history stored in MongoDB

---

## 📱 Live Demo URLs

### Development
- **Home**: `http://localhost:8000/`
- **API Docs**: `http://localhost:8000/api/docs/`
- **Admin**: `http://localhost:8000/admin/`

### Production (After Heroku Deployment)
- **Home**: `https://your-app.herokuapp.com/`
- **API Docs**: `https://your-app.herokuapp.com/api/docs/`
- **Admin**: `https://your-app.herokuapp.com/admin/`

---

**Ready for demonstration!** 🚀

