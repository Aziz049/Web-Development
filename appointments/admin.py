"""
Admin configuration for appointments app
"""
from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Custom admin for Appointment model with enhanced filters and search"""
    list_display = ('id', 'patient_name', 'doctor_name', 'branch', 'appointment_date', 
                    'appointment_time', 'status', 'is_past_display', 'created_at')
    list_filter = ('status', 'appointment_date', 'created_at', 'doctor', 'branch')
    search_fields = ('patient__email', 'patient__first_name', 'patient__last_name',
                     'doctor__email', 'doctor__first_name', 'doctor__last_name',
                     'reason', 'notes', 'branch__name')
    date_hierarchy = 'appointment_date'
    readonly_fields = ('created_at', 'updated_at', 'is_past_display')
    list_per_page = 50
    ordering = ('-appointment_date', '-appointment_time')
    
    def patient_name(self, obj):
        """Display patient full name"""
        return f"{obj.patient.get_full_name() or obj.patient.email}"
    patient_name.short_description = 'Patient'
    patient_name.admin_order_field = 'patient__first_name'
    
    def doctor_name(self, obj):
        """Display doctor full name"""
        return f"{obj.doctor.get_full_name() or obj.doctor.email}"
    doctor_name.short_description = 'Doctor'
    doctor_name.admin_order_field = 'doctor__first_name'
    
    def is_past_display(self, obj):
        """Display if appointment is past"""
        return "Yes" if obj.is_past() else "No"
    is_past_display.short_description = 'Past'
    is_past_display.boolean = True
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
        }),
        ('Additional Information', {
            'fields': ('reason', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('patient', 'doctor')


