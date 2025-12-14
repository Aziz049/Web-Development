"""
Appointment model for managing clinic appointments
"""
from django.db import models
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


class Appointment(models.Model):
    """
    Appointment model connecting patients and doctors with branch information
    """
    STATUS_CHOICES = [
        ('UPCOMING', 'Upcoming'),
        ('ATTENDED', 'Attended'),
        ('MISSED', 'Missed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),  # Legacy status for backward compatibility
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    branch = models.ForeignKey('accounts.Branch', on_delete=models.SET_NULL, null=True, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UPCOMING')
    reason = models.TextField(blank=True, null=True, help_text="Reason for appointment")
    notes = models.TextField(blank=True, null=True, help_text="Doctor's notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'appointments'
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-appointment_date', '-appointment_time']
        # Prevent double booking
        unique_together = [['doctor', 'appointment_date', 'appointment_time']]
        indexes = [
            models.Index(fields=['patient', 'appointment_date']),
            models.Index(fields=['doctor', 'appointment_date']),
            models.Index(fields=['branch', 'appointment_date']),
        ]
    
    def __str__(self):
        branch_name = self.branch.name if self.branch else "No Branch"
        return f"{self.patient.email} with {self.doctor.email} at {branch_name} on {self.appointment_date} at {self.appointment_time}"
    
    def is_past(self):
        """Check if appointment is in the past"""
        from datetime import datetime
        today = date.today()
        if self.appointment_date < today:
            return True
        if self.appointment_date == today:
            current_time = datetime.now().time()
            return self.appointment_time < current_time
        return False
    
    def clean(self):
        """Validate appointment date and time"""
        from django.core.exceptions import ValidationError
        from datetime import datetime
        
        # Prevent booking in the past
        if self.appointment_date < date.today():
            raise ValidationError("Appointment date cannot be in the past.")
        
        # Check if appointment time is in the past for today
        if self.appointment_date == date.today():
            current_time = datetime.now().time()
            if self.appointment_time < current_time:
                raise ValidationError("Appointment time cannot be in the past.")
        
        # Validate doctor belongs to the branch if branch is specified
        if self.branch and self.doctor:
            if self.doctor.is_staff() and hasattr(self.doctor, 'doctor_profile'):
                if self.doctor.doctor_profile.branch != self.branch:
                    raise ValidationError("Doctor does not belong to the selected branch.")
    
    def save(self, *args, **kwargs):
        """Override save to run validation"""
        self.full_clean()
        super().save(*args, **kwargs)

