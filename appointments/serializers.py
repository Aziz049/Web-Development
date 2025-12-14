"""
Serializers for appointments app
"""
from rest_framework import serializers
from .models import Appointment
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from datetime import date, time, datetime

User = get_user_model()


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model"""
    from accounts.serializers import BranchSerializer
    
    patient = UserSerializer(read_only=True)
    doctor = UserSerializer(read_only=True)
    branch = BranchSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True, required=False)
    doctor_id = serializers.IntegerField(write_only=True, required=False)
    branch_id = serializers.IntegerField(write_only=True, required=False)
    is_past = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = ('id', 'patient', 'doctor', 'branch', 'patient_id', 'doctor_id', 'branch_id',
                  'appointment_date', 'appointment_time', 'status', 
                  'reason', 'notes', 'is_past', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_is_past(self, obj):
        """Check if appointment is in the past"""
        return obj.is_past()
    
    def validate_appointment_date(self, value):
        """Validate appointment date"""
        if value < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value
    
    def validate(self, attrs):
        """Validate appointment data"""
        from .availability import is_time_slot_available
        
        appointment_date = attrs.get('appointment_date')
        appointment_time = attrs.get('appointment_time')
        
        # Check if appointment is in the past
        if appointment_date < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        
        if appointment_date == date.today():
            current_time = datetime.now().time()
            if appointment_time < current_time:
                raise serializers.ValidationError("Appointment time cannot be in the past.")
        
        # Check for double booking and availability
        doctor_id = attrs.get('doctor_id') or (self.instance.doctor.id if self.instance else None)
        if doctor_id and appointment_date and appointment_time:
            # Check if slot is available
            if not is_time_slot_available(doctor_id, appointment_date, appointment_time):
                raise serializers.ValidationError(
                    "This time slot is not available. Please choose another time."
                )
        
        return attrs
    
    def create(self, validated_data):
        """Create new appointment with branch validation"""
        from accounts.models import Branch
        
        request = self.context['request']
        
        # Set patient to current user if they are a patient
        if request.user.is_patient():
            validated_data['patient'] = request.user
        elif 'patient_id' in validated_data:
            validated_data['patient'] = User.objects.get(id=validated_data.pop('patient_id'))
        
        # Set doctor and validate branch
        if 'doctor_id' in validated_data:
            doctor_id = validated_data.pop('doctor_id')
            doctor = User.objects.get(id=doctor_id)
            if not doctor.is_staff():
                raise serializers.ValidationError("Selected user is not a doctor.")
            validated_data['doctor'] = doctor
            
            # Validate branch matches doctor's branch
            branch_id = validated_data.get('branch_id')
            if branch_id and hasattr(doctor, 'doctor_profile') and doctor.doctor_profile.branch:
                if doctor.doctor_profile.branch.id != branch_id:
                    raise serializers.ValidationError(
                        "Selected branch does not match doctor's assigned branch."
                    )
        
        # Set branch
        if 'branch_id' in validated_data:
            branch_id = validated_data.pop('branch_id')
            if branch_id:
                try:
                    validated_data['branch'] = Branch.objects.get(id=branch_id)
                except Branch.DoesNotExist:
                    raise serializers.ValidationError("Invalid branch ID.")
        
        # Set initial status
        validated_data['status'] = 'UPCOMING'
        
        return super().create(validated_data)


class AppointmentStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating appointment status (for doctors)"""
    
    class Meta:
        model = Appointment
        fields = ('status', 'notes')
    
    def validate_status(self, value):
        """Validate status transitions"""
        if self.instance:
            current_status = self.instance.status
            
            # Only allow certain status transitions
            if current_status == 'CANCELLED':
                raise serializers.ValidationError("Cannot change status of a cancelled appointment.")
            
            if current_status == 'COMPLETED' and value != 'COMPLETED':
                raise serializers.ValidationError("Cannot change status of a completed appointment.")
        
        return value


class VisitHistorySerializer(serializers.Serializer):
    """
    Serializer for MongoDB visit history documents.
    Note: This is not a ModelSerializer since visit history is stored in MongoDB.
    """
    _id = serializers.CharField(read_only=True)
    appointment_id = serializers.IntegerField()
    patient_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()
    visit_date = serializers.DateTimeField()
    notes = serializers.CharField(required=False, allow_blank=True)
    prescription = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def validate_prescription(self, value):
        """Allow prescription to be string or list"""
        if isinstance(value, list):
            return value
        return value or ''


class VisitHistoryCreateSerializer(serializers.Serializer):
    """
    Serializer for creating visit history records.
    """
    notes = serializers.CharField(required=False, allow_blank=True)
    prescription = serializers.CharField(required=False, allow_blank=True)
    
    def validate_prescription(self, value):
        """Allow prescription to be string or list"""
        if isinstance(value, list):
            return value
        return value or ''


