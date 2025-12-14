"""
Serializers for accounts app
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DoctorProfile, Branch, DoctorSchedule, PatientProfile, StaffProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    doctor_profile = serializers.SerializerMethodField()
    patient_profile = serializers.SerializerMethodField()
    staff_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'user_type', 'phone_number', 'date_of_birth',
                  'doctor_profile', 'patient_profile', 'staff_profile')
        read_only_fields = ('id', 'user_type')

    def get_doctor_profile(self, obj):
        """Get doctor profile if user is staff"""
        if obj.is_staff() and hasattr(obj, 'doctor_profile'):
            return DoctorProfileSerializer(obj.doctor_profile).data
        return None

    def get_patient_profile(self, obj):
        """Get patient profile if user is a patient"""
        if obj.is_patient() and hasattr(obj, 'patient_profile'):
            return PatientProfileSerializer(obj.patient_profile).data
        return None

    def get_staff_profile(self, obj):
        """Get staff profile if user is staff"""
        if obj.user_type == 'STAFF' and hasattr(obj, 'staff_profile'):
            return StaffProfileSerializer(obj.staff_profile).data
        return None


class PatientRegistrationSerializer(serializers.Serializer):
    """
    Dedicated serializer for patient registration with comprehensive validation
    """
    # Required fields
    email = serializers.EmailField(required=True, error_messages={
        'required': 'Email is required.',
        'invalid': 'Please enter a valid email address.'
    })
    username = serializers.CharField(
        required=True,
        min_length=3,
        max_length=150,
        error_messages={
            'required': 'Username is required.',
            'min_length': 'Username must be at least 3 characters long.',
            'max_length': 'Username cannot exceed 150 characters.'
        }
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 8 characters long.'
        }
    )
    password2 = serializers.CharField(
        required=True,
        write_only=True,
        label='Password Confirmation',
        error_messages={
            'required': 'Please confirm your password.'
        }
    )
    
    # Required fields
    first_name = serializers.CharField(required=True, max_length=150, error_messages={
        'required': 'First name is required.'
    })
    last_name = serializers.CharField(required=True, max_length=150, error_messages={
        'required': 'Last name is required.'
    })
    phone_number = serializers.CharField(required=False, allow_blank=True, max_length=15)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        required=False,
        allow_blank=True,
        allow_null=True
    )
    emergency_contact_name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    emergency_contact_phone = serializers.CharField(required=False, allow_blank=True, max_length=20)
    medical_conditions = serializers.CharField(required=False, allow_blank=True)
    allergies = serializers.CharField(required=False, allow_blank=True)
    current_medications = serializers.CharField(required=False, allow_blank=True)
    dental_history = serializers.CharField(required=False, allow_blank=True)
    insurance_provider = serializers.CharField(required=False, allow_blank=True, max_length=100)
    insurance_number = serializers.CharField(required=False, allow_blank=True, max_length=50)
    consent_treatment = serializers.BooleanField(required=False, default=False)
    consent_data_sharing = serializers.BooleanField(required=False, default=False)

    def validate_email(self, value):
        """Check if email already exists"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered. Please use a different email or try logging in.")
        return value

    def validate_username(self, value):
        """Check if username already exists"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken. Please choose a different username.")
        return value

    def validate_password(self, value):
        """Validate password strength"""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        # Check for at least one letter and one number
        has_letter = any(c.isalpha() for c in value)
        has_number = any(c.isdigit() for c in value)
        if not (has_letter and has_number):
            raise serializers.ValidationError("Password must contain both letters and numbers.")
        return value

    def validate(self, attrs):
        """Validate password match and consents"""
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({
                'password2': "Passwords do not match."
            })
        
        if not attrs.get('consent_treatment', False):
            raise serializers.ValidationError({
                'consent_treatment': "You must consent to treatment to proceed."
            })
        
        return attrs

    def create(self, validated_data):
        """Create user and patient profile"""
        # Remove password2 and other non-user fields
        password = validated_data.pop('password')
        validated_data.pop('password2')
        
        # Extract patient profile data
        patient_data = {
            'date_of_birth': validated_data.pop('date_of_birth', None),
            'gender': validated_data.pop('gender', None),
            'emergency_contact_name': validated_data.pop('emergency_contact_name', ''),
            'emergency_contact_phone': validated_data.pop('emergency_contact_phone', ''),
            'medical_conditions': validated_data.pop('medical_conditions', ''),
            'allergies': validated_data.pop('allergies', ''),
            'current_medications': validated_data.pop('current_medications', ''),
            'dental_history': validated_data.pop('dental_history', ''),
            'insurance_provider': validated_data.pop('insurance_provider', ''),
            'insurance_number': validated_data.pop('insurance_number', ''),
            'consent_treatment': validated_data.pop('consent_treatment', False),
            'consent_data_sharing': validated_data.pop('consent_data_sharing', False),
        }
        
        # Ensure user_type is PATIENT (explicitly set)
        validated_data['user_type'] = 'PATIENT'
        
        # Remove any is_staff references if accidentally passed
        validated_data.pop('is_staff', None)
        validated_data.pop('is_superuser', None)
        
        # Extract email and username for create_user
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        
        # Create user with explicit parameters
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            user_type='PATIENT',
            **validated_data
        )
        
        # Create patient profile
        patient_profile = PatientProfile.objects.create(
            user=user,
            **patient_data
        )
        
        return {
            'user': user,
            'patient_profile': patient_profile
        }


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users (used by Djoser)"""
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_retype = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_retype', 
                  'first_name', 'last_name', 'phone_number', 'date_of_birth', 'user_type')
    
    def validate(self, attrs):
        """Validate password match"""
        if attrs['password'] != attrs['password_retype']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs
    
    def create(self, validated_data):
        """Create new user"""
        validated_data.pop('password_retype')
        password = validated_data.pop('password')
        user_type = validated_data.pop('user_type', 'PATIENT')
        
        # Remove any is_staff or is_superuser if accidentally passed
        validated_data.pop('is_staff', None)
        validated_data.pop('is_superuser', None)
        
        # Create user with user_type, password is set by create_user
        user = User.objects.create_user(
            email=validated_data.pop('email'),
            username=validated_data.pop('username'),
            password=password,
            user_type=user_type,
            **validated_data
        )
        
        return user


class BranchSerializer(serializers.ModelSerializer):
    """Serializer for Branch model"""
    class Meta:
        model = Branch
        fields = '__all__'


class DoctorScheduleSerializer(serializers.ModelSerializer):
    """Serializer for DoctorSchedule model"""
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = DoctorSchedule
        fields = ('id', 'doctor', 'day_of_week', 'day_of_week_display', 'start_time', 'end_time', 'is_available')
        read_only_fields = ('id',)


class PatientProfileSerializer(serializers.ModelSerializer):
    """Serializer for PatientProfile model"""
    class Meta:
        model = PatientProfile
        fields = '__all__'
        read_only_fields = ('user', 'patient_id', 'created_at', 'updated_at')


class StaffProfileSerializer(serializers.ModelSerializer):
    """Serializer for StaffProfile model"""
    class Meta:
        model = StaffProfile
        fields = '__all__'
        read_only_fields = ('user', 'is_approved', 'created_at', 'updated_at')


class DoctorProfileSerializer(serializers.ModelSerializer):
    """Serializer for DoctorProfile model"""
    user = UserSerializer(read_only=True)
    branch = BranchSerializer(read_only=True)
    schedules = DoctorScheduleSerializer(many=True, read_only=True)
    user_display = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = ('id', 'user', 'user_display', 'branch', 'specialization', 'bio',
                  'years_of_experience', 'consultation_fee', 'is_available',
                  'schedules', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_user_display(self, obj):
        """Get user display name"""
        return obj.user.get_full_name() or obj.user.email


class DoctorProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating doctor profiles"""
    branch_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = DoctorProfile
        fields = ('branch_id', 'specialization', 'bio', 'years_of_experience', 
                  'consultation_fee', 'is_available')
    
    def create(self, validated_data):
        """Create doctor profile for current user"""
        user = self.context['request'].user
        if not user.is_staff():
            raise serializers.ValidationError("Only staff can create doctor profiles.")
        
        branch_id = validated_data.pop('branch_id', None)
        if branch_id:
            try:
                validated_data['branch'] = Branch.objects.get(id=branch_id)
            except Branch.DoesNotExist:
                raise serializers.ValidationError("Invalid branch ID.")
        
        doctor_profile = DoctorProfile.objects.create(
            user=user,
            **validated_data
        )
        return doctor_profile
