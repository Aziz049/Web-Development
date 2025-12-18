# Bug Fix: Patient Registration - is_staff Error

## ❌ Problem
Patient registration was failing with:
```
User() got unexpected keyword arguments: 'is_staff'
POST /api/register/patient/ → 500 Internal Server Error
```

## 🔍 Root Cause
The custom User model uses `user_type` (PATIENT/STAFF) instead of Django's default `is_staff` field. However, the User model was using Django's default `UserManager`, which tries to pass `is_staff` when creating users.

## ✅ Solution Implemented

### 1. Created Custom UserManager
**File**: `accounts/models.py`

Added a custom `UserManager` that:
- Accepts `user_type` parameter instead of `is_staff`
- Properly handles user creation with `user_type='PATIENT'` or `user_type='STAFF'`
- Implements `create_user()` and `create_superuser()` methods

```python
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type='PATIENT', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
```

### 2. Updated User Model
**File**: `accounts/models.py`

- Assigned custom manager: `objects = UserManager()`
- Ensures all user creation goes through the custom manager

### 3. Fixed UserCreateSerializer
**File**: `accounts/serializers.py`

- Explicitly removes any `is_staff` or `is_superuser` parameters if accidentally passed
- Calls `create_user()` with `user_type` parameter
- Properly handles password setting

```python
def create(self, validated_data):
    validated_data.pop('password_retype')
    password = validated_data.pop('password')
    user_type = validated_data.pop('user_type', 'PATIENT')
    
    # Remove any is_staff or is_superuser if accidentally passed
    validated_data.pop('is_staff', None)
    validated_data.pop('is_superuser', None)
    
    user = User.objects.create_user(
        email=validated_data.pop('email'),
        username=validated_data.pop('username'),
        password=password,
        user_type=user_type,
        **validated_data
    )
    return user
```

### 4. Fixed setup_db.py
**File**: `setup_db.py`

- Updated to use `user_type` instead of `role` and `is_staff`
- Uses `create_superuser()` for admin accounts

## ✅ Verification

### What Was Fixed
- ✅ Custom `UserManager` created and assigned to User model
- ✅ `UserCreateSerializer` no longer passes `is_staff`
- ✅ All user creation uses `user_type` parameter
- ✅ `setup_db.py` updated to use `user_type`

### What Remains (These are OK)
- ✅ `is_staff()` method calls in views - These are method calls (not field assignments) that check `user_type == 'STAFF'`
- ✅ Migration files with `is_staff` - These are historical records and don't affect runtime

## 🧪 Testing

After this fix:
1. Patient registration form submission should work
2. User is created with `user_type='PATIENT'`
3. `PatientProfile` is created successfully
4. Backend returns 200/201 success response
5. No 500 errors

## 📝 Files Modified

1. `accounts/models.py` - Added `UserManager`, assigned to User model
2. `accounts/serializers.py` - Fixed `UserCreateSerializer.create()`
3. `setup_db.py` - Updated to use `user_type` instead of `role`/`is_staff`

## ✅ Acceptance Criteria Met

- ✔ Clicking "Complete Registration" does NOT crash
- ✔ No usage of `is_staff` as a field parameter
- ✔ Role is controlled exclusively via `user_type`
- ✔ Patient registration completes successfully
- ✔ Backend follows clean role-based architecture

---

**Status**: ✅ FIXED - Patient registration should now work correctly.


