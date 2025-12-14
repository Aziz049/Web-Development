"""
Views for appointments app
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.utils import timezone
from datetime import date, datetime
from .models import Appointment
from .serializers import (
    AppointmentSerializer, 
    AppointmentStatusUpdateSerializer,
    VisitHistorySerializer,
    VisitHistoryCreateSerializer
)
from .mongo import (
    insert_visit_history,
    get_visit_history_by_patient,
    get_visit_history_by_doctor,
    get_all_visit_history,
    get_visit_history_by_appointment
)
from .availability import (
    get_available_time_slots,
    is_time_slot_available,
    get_doctor_availability
)


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing appointments
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient__email', 'doctor__email', 'reason', 'notes']
    ordering_fields = ['appointment_date', 'appointment_time', 'created_at']
    ordering = ['-appointment_date', '-appointment_time']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'update_status':
            return AppointmentStatusUpdateSerializer
        elif self.action == 'add_visit_history':
            return VisitHistoryCreateSerializer
        return AppointmentSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Patients can only see their own appointments
        if user.is_patient():
            queryset = queryset.filter(patient=user)
        
        # Staff can see their assigned appointments
        elif user.is_staff():
            queryset = queryset.filter(doctor=user)
        
        # Superusers can see all appointments
        elif user.is_superuser:
            queryset = queryset.all()
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by date if provided
        date_filter = self.request.query_params.get('date', None)
        if date_filter:
            queryset = queryset.filter(appointment_date=date_filter)
        
        return queryset
    
    def perform_create(self, serializer):
        """Create appointment with proper permissions"""
        user = self.request.user
        
        # Only patients can create appointments
        if not user.is_patient():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only patients can book appointments.")
        
        serializer.save(patient=user)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        """Update appointment status (for doctors)"""
        appointment = self.get_object()
        user = request.user
        
        # Only doctors can update status of their appointments
        if not user.is_doctor() or appointment.doctor != user:
            return Response(
                {"error": "Only the assigned doctor can update appointment status."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Prevent updating past appointments to UPCOMING
        new_status = request.data.get('status')
        if new_status == 'UPCOMING' and appointment.is_past():
            return Response(
                {"error": "Cannot set past appointments to upcoming status."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = AppointmentStatusUpdateSerializer(
            appointment, 
            data=request.data, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        """Cancel appointment (for patients)"""
        appointment = self.get_object()
        user = request.user
        
        # Only patients can cancel their own appointments
        if not user.is_patient() or appointment.patient != user:
            return Response(
                {"error": "You can only cancel your own appointments."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Cannot cancel completed or already cancelled appointments
        if appointment.status in ['COMPLETED', 'CANCELLED']:
            return Response(
                {"error": f"Cannot cancel an appointment with status: {appointment.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.status = 'CANCELLED'
        appointment.save()
        
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_appointments(self, request):
        """Get current user's appointments"""
        user = request.user
        
        if user.is_patient():
            appointments = Appointment.objects.filter(patient=user)
        elif user.is_staff():
            appointments = Appointment.objects.filter(doctor=user)
        else:
            appointments = Appointment.objects.none()
        
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def upcoming(self, request):
        """Get upcoming appointments"""
        user = request.user
        today = date.today()
        current_time = datetime.now().time()
        
        if user.is_patient():
            appointments = Appointment.objects.filter(
                patient=user,
                appointment_date__gte=today
            ).exclude(status='CANCELLED')
        elif user.is_staff():
            appointments = Appointment.objects.filter(
                doctor=user,
                appointment_date__gte=today
            ).exclude(status='CANCELLED')
        else:
            appointments = Appointment.objects.none()
        
        # Filter out past appointments for today
        appointments = [
            apt for apt in appointments 
            if apt.appointment_date > today or 
            (apt.appointment_date == today and apt.appointment_time >= current_time)
        ]
        
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def reports(self, request):
        """Get appointment reports (for admins)"""
        if not request.user.is_superuser:
            return Response(
                {"error": "Only admins can access reports."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Appointments per doctor
        appointments_per_doctor = Appointment.objects.values(
            'doctor__email', 
            'doctor__first_name', 
            'doctor__last_name'
        ).annotate(
            total_appointments=Count('id'),
            confirmed=Count('id', filter=Q(status='CONFIRMED')),
            completed=Count('id', filter=Q(status='COMPLETED')),
            pending=Count('id', filter=Q(status='PENDING')),
            cancelled=Count('id', filter=Q(status='CANCELLED'))
        ).order_by('-total_appointments')
        
        # Total appointments by status
        status_counts = Appointment.objects.values('status').annotate(
            count=Count('id')
        )
        
        return Response({
            'appointments_per_doctor': list(appointments_per_doctor),
            'status_counts': list(status_counts),
            'total_appointments': Appointment.objects.count(),
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def history(self, request):
        """
        Get appointment history for current user.
        Patients see their own history, doctors see their appointments, admins see all.
        """
        user = request.user
        today = date.today()
        
        if user.is_patient():
            # Patients see all their appointments (upcoming and past)
            appointments = Appointment.objects.filter(patient=user).order_by('-appointment_date', '-appointment_time')
        elif user.is_staff():
            # Staff see all their appointments
            appointments = Appointment.objects.filter(doctor=user).order_by('-appointment_date', '-appointment_time')
        elif user.is_superuser:
            # Superusers see all appointments
            appointments = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')
        else:
            appointments = Appointment.objects.none()
        
        # Filter by status if provided
        status_filter = request.query_params.get('status', None)
        if status_filter:
            appointments = appointments.filter(status=status_filter)
        
        # Separate upcoming and past
        upcoming = [apt for apt in appointments if not apt.is_past()]
        past = [apt for apt in appointments if apt.is_past()]
        
        serializer = self.get_serializer(appointments, many=True)
        
        return Response({
            'upcoming': self.get_serializer(upcoming, many=True).data,
            'past': self.get_serializer(past, many=True).data,
            'all': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_attended(self, request, pk=None):
        """Mark appointment as attended (for doctors)"""
        appointment = self.get_object()
        user = request.user
        
        if not user.is_staff() or appointment.doctor != user:
            return Response(
                {"error": "Only the assigned staff member can mark appointments as attended."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if appointment.is_past():
            appointment.status = 'ATTENDED'
            appointment.save()
            serializer = self.get_serializer(appointment)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Cannot mark future appointments as attended."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_missed(self, request, pk=None):
        """Mark appointment as missed (for doctors)"""
        appointment = self.get_object()
        user = request.user
        
        if not user.is_staff() or appointment.doctor != user:
            return Response(
                {"error": "Only the assigned staff member can mark appointments as missed."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if appointment.is_past():
            appointment.status = 'MISSED'
            appointment.save()
            serializer = self.get_serializer(appointment)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Cannot mark future appointments as missed."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_visit_history(self, request, pk=None):
        """
        Add visit history for a completed appointment (MongoDB).
        Only doctors can add visit history, and only for completed appointments.
        """
        appointment = self.get_object()
        user = request.user
        
        # Only staff can add visit history
        if not user.is_staff():
            return Response(
                {"error": "Only staff can add visit history."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Only the assigned doctor can add visit history
        if appointment.doctor != user:
            return Response(
                {"error": "You can only add visit history for your own appointments."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Only allow visit history for completed appointments
        if appointment.status != 'COMPLETED':
            return Response(
                {"error": "Visit history can only be added for completed appointments."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if visit history already exists
        existing_history = get_visit_history_by_appointment(appointment.id)
        if existing_history:
            return Response(
                {"error": "Visit history already exists for this appointment."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate input
        serializer = VisitHistoryCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Insert visit history into MongoDB
        try:
            visit_record = insert_visit_history(
                appointment_id=appointment.id,
                patient_id=appointment.patient.id,
                doctor_id=appointment.doctor.id,
                visit_date=appointment.appointment_date,
                notes=serializer.validated_data.get('notes', ''),
                prescription=serializer.validated_data.get('prescription', '')
            )
            
            # Serialize and return the created record
            response_serializer = VisitHistorySerializer(visit_record)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {"error": f"Failed to save visit history: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

