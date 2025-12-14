"""
Custom User model with roles (Patient, Doctor, Admin)
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class UserManager(BaseUserManager):
    """
    Custom user manager that uses user_type instead of is_staff
    """
    def create_user(self, email, password=None, user_type='PATIENT', **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('user_type', 'STAFF')
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with simplified permission model.
    User Types: PATIENT, STAFF
    Staff includes doctors, nurses, administrators, etc.
    """
    USER_TYPE_CHOICES = [
        ('PATIENT', 'Patient'),
        ('STAFF', 'Staff'),
    ]
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='PATIENT')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.email} ({self.user_type})"
    
    def is_patient(self):
        """Check if user is a patient"""
        return self.user_type == 'PATIENT'
    
    def is_staff(self):
        """Check if user is staff (includes doctors, nurses, admins)"""
        return self.user_type == 'STAFF' and self.is_active
    
    def is_approved_staff(self):
        """Check if user is approved staff (active and approved)"""
        if not self.is_staff():
            return False
        if hasattr(self, 'staff_profile'):
            return self.staff_profile.is_approved
        return False
    
    # Backward compatibility methods (for existing code)
    def is_doctor(self):
        """Backward compatibility - staff can be doctors"""
        return self.is_staff()
    
    def is_admin(self):
        """Backward compatibility - check if user is staff and superuser"""
        return self.is_staff() and self.is_superuser


class Branch(models.Model):
    """
    Clinic branch/location model
    """
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'branches'
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    """
    Extended profile for doctors with specialization, branch, and availability
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors')
    specialization = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    years_of_experience = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'doctor_profiles'
        verbose_name = 'Doctor Profile'
        verbose_name_plural = 'Doctor Profiles'
    
    def __str__(self):
        branch_name = self.branch.name if self.branch else "No Branch"
        return f"{self.user.get_full_name() or self.user.email} - {self.specialization} ({branch_name})"


class DoctorSchedule(models.Model):
    """
    Doctor's weekly schedule defining available days and time ranges
    """
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'doctor_schedules'
        verbose_name = 'Doctor Schedule'
        verbose_name_plural = 'Doctor Schedules'
        unique_together = [['doctor', 'day_of_week']]
        ordering = ['doctor', 'day_of_week', 'start_time']
    
    def __str__(self):
        day_name = dict(self.DAY_CHOICES)[self.day_of_week]
        return f"{self.doctor.user.get_full_name()} - {day_name} ({self.start_time} - {self.end_time})"


class PatientProfile(models.Model):
    """
    Extended profile for patients with medical and dental information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    patient_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True, help_text="List any medical conditions")
    allergies = models.TextField(blank=True, null=True, help_text="List any allergies")
    current_medications = models.TextField(blank=True, null=True, help_text="Current medications")
    dental_history = models.TextField(blank=True, null=True, help_text="Previous dental treatments")
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
    insurance_number = models.CharField(max_length=50, blank=True, null=True)
    consent_treatment = models.BooleanField(default=False)
    consent_data_sharing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patient_profiles'
        verbose_name = 'Patient Profile'
        verbose_name_plural = 'Patient Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} - {self.patient_id or 'No ID'}"
    
    def save(self, *args, **kwargs):
        """Auto-generate patient ID if not provided"""
        if not self.patient_id:
            # Generate patient ID: PAT-YYYYMMDD-XXXX
            from datetime import datetime
            prefix = "PAT"
            date_part = datetime.now().strftime("%Y%m%d")
            # Get last patient ID for today
            last_patient = PatientProfile.objects.filter(
                patient_id__startswith=f"{prefix}-{date_part}"
            ).order_by('-patient_id').first()
            
            if last_patient and last_patient.patient_id:
                try:
                    last_num = int(last_patient.patient_id.split('-')[-1])
                    new_num = last_num + 1
                except (ValueError, IndexError):
                    new_num = 1
            else:
                new_num = 1
            
            self.patient_id = f"{prefix}-{date_part}-{new_num:04d}"
        
        super().save(*args, **kwargs)


class StaffProfile(models.Model):
    """
    Extended profile for staff members (doctors, nurses, admin, etc.)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    role_title = models.CharField(max_length=100, help_text="Job title (e.g., Senior Dentist, Nurse)")
    department = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    license_expiry = models.DateField(blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False, help_text="Admin approval required")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_staff')
    approved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'staff_profiles'
        verbose_name = 'Staff Profile'
        verbose_name_plural = 'Staff Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} - {self.employee_id}"


class StaffAuthorizationAttempt(models.Model):
    """
    Track staff authorization attempts for security
    """
    ip_address = models.GenericIPAddressField()
    employee_id = models.CharField(max_length=20)
    registration_code = models.CharField(max_length=50)
    success = models.BooleanField(default=False)
    attempt_count = models.IntegerField(default=1)
    locked_until = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'staff_authorization_attempts'
        verbose_name = 'Staff Authorization Attempt'
        verbose_name_plural = 'Staff Authorization Attempts'
        indexes = [
            models.Index(fields=['ip_address', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.ip_address} - {self.employee_id} - {'Success' if self.success else 'Failed'}"


class RegistrationAttempt(models.Model):
    """
    Track all registration attempts for security and analytics
    """
    ip_address = models.GenericIPAddressField()
    user_type = models.CharField(max_length=10, choices=User.USER_TYPE_CHOICES)
    email = models.EmailField(blank=True, null=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'registration_attempts'
        verbose_name = 'Registration Attempt'
        verbose_name_plural = 'Registration Attempts'
        indexes = [
            models.Index(fields=['ip_address', 'created_at']),
            models.Index(fields=['user_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.ip_address} - {self.user_type} - {'Success' if self.success else 'Failed'}"


