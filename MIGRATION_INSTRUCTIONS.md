# Migration Instructions - Fix Authentication Errors

## 🚨 Critical Fix Required

The database schema is outdated. The `users` table has a `role` column but the code expects `user_type`.

## ✅ Steps to Fix

### 1. Create Migration
A migration file has been created: `accounts/migrations/0003_user_user_type_remove_user_role.py`

This migration will:
- Add `user_type` field to User model
- Migrate existing data from `role` to `user_type`
- Remove the old `role` field

### 2. Apply Migration

Run these commands in order:

```bash
# Make sure you're in the project root directory
cd "Web Development final project"

# Create any additional migrations if needed
python manage.py makemigrations

# Apply the migration
python manage.py migrate

# If you get errors about existing data, you may need to:
# Option A: If you have no important data, reset the database:
python manage.py flush
python manage.py migrate

# Option B: If you have important data, the migration includes data migration
# that will convert role values to user_type values automatically
```

### 3. Verify Migration

After migration, verify the schema:

```bash
# Check if migration was applied
python manage.py showmigrations accounts

# You should see:
# [X] 0001_initial
# [X] 0002_branch_doctorprofile_branch_doctorschedule
# [X] 0003_user_user_type_remove_user_role
```

### 4. Test Registration

1. Start the server:
   ```bash
   python manage.py runserver
   ```

2. Visit: http://localhost:8000/access/
3. Select "Patient"
4. Complete registration form
5. Should see success message and redirect to login

## ✅ What Was Fixed

1. **Database Schema**: Migration adds `user_type` column
2. **Data Migration**: Existing `role` values converted to `user_type`
3. **Error Handling**: User-friendly error messages in registration
4. **DRF Browsable API**: Already disabled (JSON only)
5. **Custom UserManager**: Already implemented (handles `user_type`)

## 🔍 Verification Checklist

After migration, verify:

- [ ] `python manage.py migrate` runs without errors
- [ ] Patient registration works (no 500 errors)
- [ ] User is created with `user_type='PATIENT'`
- [ ] No `is_staff` parameter errors
- [ ] Success message shown and redirects to login
- [ ] No DRF browsable API visible
- [ ] Error messages are user-friendly

## ⚠️ If Migration Fails

If you get errors during migration:

1. **Backup your database** (if you have important data)
2. **Check for existing users** with `role` field
3. **Run migration in steps**:
   ```bash
   # Step 1: Add user_type field
   # Step 2: Migrate data
   # Step 3: Remove role field
   ```

4. **If all else fails**, reset database:
   ```bash
   python manage.py flush
   python manage.py migrate
   python manage.py createsuperuser
   ```

---

**Status**: ✅ Migration file created and ready to apply


