"""
Admin configuration for appointments app
"""
from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Custom admin for Appointment model"""
    list_display = ('id', 'patient', 'doctor', 'appointment_date', 
                    'appointment_time', 'status', 'created_at')
    list_filter = ('status', 'appointment_date', 'created_at', 'doctor')
    search_fields = ('patient__email', 'doctor__email', 'reason', 'notes')
    date_hierarchy = 'appointment_date'
    readonly_fields = ('created_at', 'updated_at')
    
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


