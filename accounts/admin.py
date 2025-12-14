"""
Admin configuration for accounts app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, DoctorProfile, Branch, DoctorSchedule,
    PatientProfile, StaffProfile, StaffAuthorizationAttempt, RegistrationAttempt
)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """Admin for Branch model"""
    list_display = ('name', 'address', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'address', 'phone', 'email')
    ordering = ('name',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    list_display = ('email', 'username', 'user_type', 'is_active', 'is_superuser', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_superuser', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'date_of_birth')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('email', 'user_type', 'phone_number', 'date_of_birth')}),
    )


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    """Admin for DoctorProfile model"""
    list_display = ('user', 'branch', 'specialization', 'years_of_experience', 'consultation_fee', 'is_available')
    list_filter = ('branch', 'specialization', 'is_available', 'years_of_experience')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'specialization', 'branch__name')
    raw_id_fields = ('user', 'branch')


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    """Admin for DoctorSchedule model"""
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time', 'is_available')
    list_filter = ('day_of_week', 'is_available', 'doctor__branch')
    search_fields = ('doctor__user__email', 'doctor__user__first_name', 'doctor__user__last_name')
    raw_id_fields = ('doctor',)


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    """Admin for PatientProfile model"""
    list_display = ('patient_id', 'user', 'date_of_birth', 'gender', 'consent_treatment', 'created_at')
    list_filter = ('gender', 'consent_treatment', 'consent_data_sharing', 'created_at')
    search_fields = ('patient_id', 'user__email', 'user__first_name', 'user__last_name', 'insurance_number')
    raw_id_fields = ('user',)
    readonly_fields = ('patient_id', 'created_at', 'updated_at')


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    """Admin for StaffProfile model"""
    list_display = ('employee_id', 'user', 'role_title', 'department', 'is_approved', 'mfa_enabled', 'created_at')
    list_filter = ('is_approved', 'mfa_enabled', 'department', 'role_title', 'created_at')
    search_fields = ('employee_id', 'user__email', 'user__first_name', 'user__last_name', 'license_number')
    raw_id_fields = ('user', 'approved_by')
    readonly_fields = ('created_at', 'updated_at', 'approved_at')


@admin.register(StaffAuthorizationAttempt)
class StaffAuthorizationAttemptAdmin(admin.ModelAdmin):
    """Admin for StaffAuthorizationAttempt model"""
    list_display = ('ip_address', 'employee_id', 'success', 'attempt_count', 'locked_until', 'created_at')
    list_filter = ('success', 'created_at')
    search_fields = ('ip_address', 'employee_id')
    readonly_fields = ('created_at',)


@admin.register(RegistrationAttempt)
class RegistrationAttemptAdmin(admin.ModelAdmin):
    """Admin for RegistrationAttempt model"""
    list_display = ('ip_address', 'user_type', 'email', 'success', 'created_at')
    list_filter = ('user_type', 'success', 'created_at')
    search_fields = ('ip_address', 'email')
    readonly_fields = ('created_at',)


# ============================================================================
# REFACTOR: Staff Approval System - Admin Only
# ============================================================================

@admin.action(description='Approve selected staff accounts')
def approve_staff(modeladmin, request, queryset):
    """Approve staff accounts and send activation email"""
    from django.core.mail import send_mail
    from django.conf import settings
    
    approved_count = 0
    for staff_profile in queryset:
        if not staff_profile.is_approved:
            staff_profile.is_approved = True
            staff_profile.approved_by = request.user
            staff_profile.approved_at = timezone.now()
            staff_profile.save()
            
            # Activate user account
            user = staff_profile.user
            user.is_active = True
            user.save()
            
            # Send activation email
            try:
                send_mail(
                    subject='Your Staff Account Has Been Approved - Apex Dental Care',
                    message=f'''
Dear {user.get_full_name() or user.email},

Your staff account at Apex Dental Care has been approved and activated.

You can now log in using:
Email: {user.email}
Username: {user.username}

Please log in and complete your profile setup.

Best regards,
Apex Dental Care Administration
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@apexdental.com',
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception:
                pass  # Email sending is optional
            
            approved_count += 1
    
    modeladmin.message_user(request, f'{approved_count} staff account(s) approved and activated.')


@admin.action(description='Reject selected staff accounts')
def reject_staff(modeladmin, request, queryset):
    """Reject staff accounts"""
    rejected_count = 0
    for staff_profile in queryset:
        if not staff_profile.is_approved:
            # Delete the user account
            staff_profile.user.delete()
            rejected_count += 1
    
    modeladmin.message_user(request, f'{rejected_count} staff account(s) rejected and removed.')


# Custom admin for staff approval
class StaffProfileApprovalAdmin(admin.ModelAdmin):
    """Admin interface for staff approval - shows only pending accounts"""
    list_display = ('employee_id', 'user', 'role_title', 'department', 'email', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'department', 'role_title', 'created_at')
    search_fields = ('employee_id', 'user__email', 'user__first_name', 'user__last_name', 'role_title')
    raw_id_fields = ('user', 'approved_by')
    readonly_fields = ('created_at', 'updated_at', 'approved_at')
    actions = [approve_staff, reject_staff]
    
    def get_queryset(self, request):
        """Show pending staff accounts first"""
        qs = super().get_queryset(request)
        return qs.order_by('is_approved', '-created_at')
    
    def email(self, obj):
        """Display user email"""
        return obj.user.email
    email.short_description = 'Email'
    
    def has_add_permission(self, request):
        """Only superusers can add staff profiles"""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Only superusers can change staff profiles"""
        return request.user.is_superuser


# Unregister and re-register with custom admin
admin.site.unregister(StaffProfile)
admin.site.register(StaffProfile, StaffProfileApprovalAdmin)


