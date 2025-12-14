# MongoDB Visit History Setup

## Overview

This project uses **polyglot persistence** - PostgreSQL for structured data (users, appointments) and MongoDB for unstructured data (visit history).

## MongoDB Atlas Setup

1. **Create MongoDB Atlas Account**
   - Go to https://www.mongodb.com/cloud/atlas
   - Sign up for a free account

2. **Create a Cluster**
   - Create a free M0 cluster
   - Choose your preferred region

3. **Create Database User**
   - Go to Database Access
   - Add a new database user
   - Username: `VigilantEye` (or your choice)
   - Password: `Vigi@Expo49` (or your choice)
   - Save the credentials

4. **Whitelist IP Address**
   - Go to Network Access
   - Add IP Address: `0.0.0.0/0` (for development) or your specific IP
   - Click "Add IP Address"

5. **Get Connection String**
   - Go to Clusters → Connect
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your actual password (URL-encoded if needed)

## Environment Variables

Add to your `.env` file:

```env
MONGODB_URI=mongodb+srv://VigilantEye:Vigi%40Expo49@cluster0.pomckdi.mongodb.net/?appName=Cluster0
MONGODB_DB_NAME=clinic_appointment
MONGODB_COLLECTION_NAME=visit_history
```

**Important**: URL-encode special characters in password:
- `@` becomes `%40`
- `#` becomes `%23`
- `$` becomes `%24`
- etc.

## Visit History Feature

### Data Structure

Each visit history document in MongoDB contains:
```json
{
  "_id": "ObjectId",
  "appointment_id": 123,
  "patient_id": 1,
  "doctor_id": 2,
  "visit_date": "2024-01-15T10:00:00",
  "notes": "Patient showed improvement...",
  "prescription": "Take medication twice daily",
  "created_at": "2024-01-15T10:30:00"
}
```

### API Endpoints

#### Add Visit History
```bash
POST /api/api/appointments/{id}/add_visit_history/
Authorization: Bearer <doctor_token>

Body:
{
  "notes": "Patient condition improved",
  "prescription": "Continue medication for 5 days"
}
```

**Requirements:**
- Only doctors can add visit history
- Appointment must be completed
- Only the assigned doctor can add history

#### View Visit History
```bash
GET /api/api/visit-history/
Authorization: Bearer <token>
```

**Access Control:**
- **Patients**: See only their own visit history
- **Doctors**: See visit history for their patients
- **Admins**: See all visit history records

## Testing

1. **Complete an appointment** (as doctor):
   ```bash
   PATCH /api/api/appointments/{id}/update_status/
   Body: {"status": "COMPLETED"}
   ```

2. **Add visit history** (as doctor):
   ```bash
   POST /api/api/appointments/{id}/add_visit_history/
   Body: {
     "notes": "Patient responded well to treatment",
     "prescription": "Continue medication"
   }
   ```

3. **View visit history** (as patient/doctor/admin):
   ```bash
   GET /api/api/visit-history/
   ```

## Troubleshooting

### Connection Errors
- Verify MongoDB Atlas cluster is running
- Check IP whitelist includes your IP
- Verify username/password are correct
- Ensure password is URL-encoded in connection string

### Permission Errors
- Ensure user has correct role (doctor for adding history)
- Verify appointment status is "COMPLETED"
- Check JWT token is valid

### Data Not Appearing
- Check MongoDB Atlas dashboard to verify documents were created
- Verify collection name matches `MONGODB_COLLECTION_NAME`
- Check database name matches `MONGODB_DB_NAME`

## Architecture Notes

- **PostgreSQL**: Used for structured relational data (users, appointments)
- **MongoDB**: Used for unstructured document data (visit history)
- **No Django Models**: Visit history is stored directly in MongoDB, not as Django models
- **PyMongo**: Direct MongoDB driver, no ORM layer
- **Serializers**: Custom serializers handle MongoDB document serialization

This demonstrates **polyglot persistence** - using the right database for the right data type.

