# Railway Deployment Verification Checklist

## ✅ Pre-Deployment Checks

- [x] `dj-database-url` added to requirements.txt
- [x] `DATABASE_URL` configuration in settings.py
- [x] `Procfile` updated for Railway (`$PORT`)
- [x] `railway.json` and `railway.toml` created
- [x] Static files configured (WhiteNoise)
- [x] CORS and CSRF settings for Railway domains
- [x] Production security settings added
- [x] Environment variables documented

---

## 🧪 Post-Deployment Verification

After deploying to Railway, verify these endpoints work:

### 1. Home Page
```
https://your-app-name.up.railway.app/
```
**Expected**: Home page loads with clinic information

### 2. API Documentation
```
https://your-app-name.up.railway.app/api/docs/
```
**Expected**: Swagger UI loads and shows all endpoints

### 3. Admin Panel
```
https://your-app-name.up.railway.app/admin/
```
**Expected**: Django admin login page

### 4. Patient Registration
```
https://your-app-name.up.railway.app/access/patient/
```
**Expected**: Registration form loads

### 5. API Endpoints

**Login:**
```bash
curl -X POST https://your-app-name.up.railway.app/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```
**Expected**: Returns JWT tokens

**List Appointments (with token):**
```bash
curl -X GET https://your-app-name.up.railway.app/api/appointments/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
**Expected**: Returns appointments list (or empty if no data)

---

## 🔍 Common Issues & Fixes

### Issue: Database Connection Error
**Fix**: 
1. Verify PostgreSQL service is running in Railway
2. Check `DATABASE_URL` is set (Railway sets this automatically)
3. Run migrations: `railway run python manage.py migrate`

### Issue: Static Files 404
**Fix**:
1. Check deployment logs for `collectstatic` output
2. Verify `STATIC_ROOT` is correct
3. Ensure WhiteNoise middleware is enabled

### Issue: CORS Errors
**Fix**:
1. Add frontend domain to `CORS_ALLOWED_ORIGINS`
2. Add Railway domain to `CSRF_TRUSTED_ORIGINS`

### Issue: 500 Internal Server Error
**Fix**:
1. Check Railway logs
2. Verify `SECRET_KEY` is set
3. Verify `DEBUG=False` in production
4. Check database migrations completed

---

## 📊 Verification Steps

1. **Deploy to Railway**
2. **Run Migrations**: Use Railway shell or CLI
3. **Create Superuser**: `railway run python manage.py createsuperuser`
4. **Test Registration**: Register a new patient
5. **Test Login**: Login with created account
6. **Test API**: Use Swagger UI or Postman
7. **Test Admin**: Login to admin panel
8. **Test Booking**: Book an appointment
9. **Check Logs**: Monitor Railway logs for errors

---

## ✅ Success Criteria

- [ ] Home page loads
- [ ] API documentation accessible
- [ ] Patient registration works
- [ ] JWT login works
- [ ] Appointment booking works
- [ ] Admin panel accessible
- [ ] Static files load correctly
- [ ] No 500 errors in logs
- [ ] Database queries work
- [ ] All API endpoints respond

---

**If all checks pass, deployment is successful!** 🎉


