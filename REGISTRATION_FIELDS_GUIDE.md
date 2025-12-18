# Patient Registration - Required Fields & Examples

## ✅ Required Fields (Must Fill)

### 1. **Personal Information** (Step 1)
- `first_name` - **Required**
  - Example: `"John"`
  - Type: Text (max 150 characters)

- `last_name` - **Required**
  - Example: `"Doe"`
  - Type: Text (max 150 characters)

- `date_of_birth` - **Required**
  - Example: `"1990-05-15"`
  - Format: YYYY-MM-DD
  - Cannot be in the future
  - Cannot be more than 120 years ago

- `gender` - **Optional**
  - Example: `"M"` (Male), `"F"` (Female), `"O"` (Other)
  - Can be left empty

### 2. **Contact Details** (Step 2)
- `username` - **Required**
  - Example: `"johndoe123"`
  - Type: Text
  - Minimum: 3 characters
  - Maximum: 150 characters
  - Must be unique (not already taken)

- `email` - **Required**
  - Example: `"john.doe@example.com"`
  - Type: Email
  - Must be valid email format
  - Must be unique (not already registered)

- `phone_number` - **Required**
  - Example: `"+96512345678"` or `"12345678"`
  - Type: Text (max 15 characters)
  - Can include country code

- `emergency_contact_name` - **Optional**
  - Example: `"Jane Doe"`
  - Can be left empty

- `emergency_contact_phone` - **Optional**
  - Example: `"+96598765432"`
  - Can be left empty

### 3. **Medical & Dental Info** (Step 3) - All Optional
- `medical_conditions` - Optional
  - Example: `"Diabetes, Hypertension"`
  - Can be left empty

- `allergies` - Optional
  - Example: `"Penicillin, Latex"`
  - Can be left empty

- `current_medications` - Optional
  - Example: `"Aspirin 100mg daily"`
  - Can be left empty

- `dental_history` - Optional
  - Example: `"Root canal in 2020"`
  - Can be left empty

- `insurance_provider` - Optional
  - Example: `"Kuwait Insurance Company"`
  - Can be left empty

- `insurance_number` - Optional
  - Example: `"INS-123456"`
  - Can be left empty

### 4. **Account Security** (Step 4)
- `password` - **Required**
  - Example: `"SecurePass123"`
  - Minimum: 8 characters
  - Must contain: At least one letter AND one number
  - Valid examples: `"Password1"`, `"MyPass123"`, `"Secure2024"`
  - Invalid examples: `"password"` (no number), `"12345678"` (no letters), `"short"` (too short)

- `re_password` - **Required**
  - Example: `"SecurePass123"` (must match password exactly)
  - Must be identical to `password`

### 5. **Consents** (Step 5)
- `consent_treatment` - **Required**
  - Example: `true` (checkbox must be checked)
  - Must be checked to proceed

- `consent_data_sharing` - **Optional**
  - Example: `true` or `false`
  - Can be left unchecked

## 📋 Complete Example JSON

Here's a complete example of valid registration data:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-05-15",
  "gender": "M",
  "username": "johndoe123",
  "email": "john.doe@example.com",
  "phone_number": "+96512345678",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+96598765432",
  "medical_conditions": "Diabetes",
  "allergies": "Penicillin",
  "current_medications": "Aspirin 100mg daily",
  "dental_history": "Root canal in 2020",
  "insurance_provider": "Kuwait Insurance",
  "insurance_number": "INS-123456",
  "password": "SecurePass123",
  "re_password": "SecurePass123",
  "consent_treatment": true,
  "consent_data_sharing": true
}
```

## ⚠️ Common Errors & Solutions

### Error: "Email is required"
- **Solution**: Make sure you fill the email field in Step 2

### Error: "Username is required"
- **Solution**: Make sure you fill the username field in Step 2 (only one username field exists)

### Error: "Password must be at least 8 characters long"
- **Solution**: Use a password with 8+ characters, e.g., `"MyPass123"`

### Error: "Password must contain both letters and numbers"
- **Solution**: Include both letters and numbers, e.g., `"Password1"` ✅ NOT `"password"` ❌

### Error: "Passwords do not match"
- **Solution**: Make sure `password` and `re_password` are exactly the same

### Error: "This email is already registered"
- **Solution**: Use a different email address or try logging in instead

### Error: "This username is already taken"
- **Solution**: Choose a different username

### Error: "You must consent to treatment to proceed"
- **Solution**: Check the consent checkbox in Step 5

## 🔍 Field Validation Rules

| Field | Required | Min Length | Max Length | Format | Example |
|-------|----------|------------|------------|--------|---------|
| first_name | ✅ Yes | - | 150 | Text | "John" |
| last_name | ✅ Yes | - | 150 | Text | "Doe" |
| date_of_birth | ✅ Yes | - | - | YYYY-MM-DD | "1990-05-15" |
| gender | ❌ No | - | - | M/F/O | "M" |
| username | ✅ Yes | 3 | 150 | Text | "johndoe123" |
| email | ✅ Yes | - | - | Email | "john@example.com" |
| phone_number | ✅ Yes | - | 15 | Text | "+96512345678" |
| password | ✅ Yes | 8 | - | Text (letters+numbers) | "SecurePass123" |
| re_password | ✅ Yes | 8 | - | Text (must match password) | "SecurePass123" |
| consent_treatment | ✅ Yes | - | - | Boolean | true |

## ✅ Quick Test Data

**Minimal Required Fields:**
```json
{
  "first_name": "Test",
  "last_name": "User",
  "date_of_birth": "1990-01-01",
  "username": "testuser123",
  "email": "testuser@example.com",
  "phone_number": "12345678",
  "password": "TestPass123",
  "re_password": "TestPass123",
  "consent_treatment": true
}
```

---

**Note**: All other fields are optional and can be left empty or omitted.


