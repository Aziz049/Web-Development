"""
API Views for Registration Endpoints
These are REST API endpoints (not HTML forms) for programmatic access
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import PatientProfile, StaffProfile, RegistrationAttempt
from .serializers import (
    PatientRegistrationSerializer,
    UserSerializer
)
from decouple import config
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def api_register_patient(request):
    """
    API endpoint for patient registration with auto-login
    
    POST /api/auth/register/patient/
    
    Request Body:
    {
        "email": "patient@example.com",
        "username": "patient123",
        "password": "SecurePass123",
        "password2": "SecurePass123",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+96512345678",
        "date_of_birth": "1990-05-15",
        "gender": "M",
        "consent_treatment": true
    }
    
    Response (201):
    {
        "success": true,
        "message": "Registration successful! Your Patient ID is: PAT-001",
        "access": "<JWT access token>",
        "refresh": "<JWT refresh token>",
        "user": {
            "id": 1,
            "email": "patient@example.com",
            "username": "patient123",
            "first_name": "John",
            "last_name": "Doe",
            "user_type": "PATIENT"
        },
        "patient_id": "PAT-001"
    }
    """
    try:
        serializer = PatientRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            result = serializer.save()
            user = result['user']
            patient_profile = result['patient_profile']
            
            # Track registration attempt
            ip_address = request.META.get('REMOTE_ADDR')
            try:
                RegistrationAttempt.objects.create(
                    ip_address=ip_address,
                    user_type='PATIENT',
                    email=user.email,
                    success=True
                )
            except Exception:
                pass
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Serialize user data
            user_serializer = UserSerializer(user)
            
            return Response({
                'success': True,
                'message': f'Registration successful! Your Patient ID is: {patient_profile.patient_id}',
                'access': access_token,
                'refresh': refresh_token,
                'user': user_serializer.data,
                'patient_id': patient_profile.patient_id
            }, status=status.HTTP_201_CREATED)
        else:
            # Return field-specific errors
            errors = {}
            for field, error_list in serializer.errors.items():
                if isinstance(error_list, list):
                    errors[field] = error_list[0] if error_list else 'Invalid value'
                else:
                    errors[field] = str(error_list)
            
            return Response({
                'success': False,
                'errors': errors,
                'error': 'Please correct the errors below and try again.'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.error(f"Patient registration error: {e}", exc_info=True)
        return Response({
            'success': False,
            'error': 'Registration failed. Please try again later.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_register_staff(request):
    """
    API endpoint for staff registration (requires admin approval)
    
    POST /api/auth/register/staff/
    
    Note: Staff registration requires prior authorization via /api/staff/authorize/
    
    Request Body:
    {
        "email": "doctor@apexdental.com",
        "username": "doctor123",
        "password": "SecurePass123456",
        "password2": "SecurePass123456",
        "first_name": "Jane",
        "last_name": "Smith",
        "phone_number": "+96512345678",
        "employee_id": "DOC001",
        "role_title": "Orthodontist",
        "department": "Dental",
        "specialization": "Orthodontics",
        "license_number": "LIC123456"
    }
    
    Response (201):
    {
        "success": true,
        "message": "Registration submitted successfully. Your account is pending admin approval.",
        "employee_id": "DOC001"
    }
    """
    # Check if staff was authorized (in production, use session or token)
    # For API, we'll require a separate authorization step
    employee_id = request.data.get('employee_id')
    if not employee_id:
        return Response({
            'success': False,
            'error': 'Employee ID is required. Please complete authorization first.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Validate email domain
        email = request.data.get('email', '')
        if not email.endswith(config('CLINIC_EMAIL_DOMAIN', default='@apexdental.com')):
            return Response({
                'success': False,
                'error': 'Invalid email domain. Staff must use clinic email address.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate password strength (12+ chars for staff)
        password = request.data.get('password', '')
        if len(password) < 12:
            return Response({
                'success': False,
                'error': 'Password must be at least 12 characters long for staff accounts.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use UserCreateSerializer for user creation
        from .serializers import UserCreateSerializer
        
        user_data = {
            'username': request.data.get('username'),
            'email': email,
            'password': password,
            'password_retype': request.data.get('password2', ''),
            'first_name': request.data.get('first_name', ''),
            'last_name': request.data.get('last_name', ''),
            'phone_number': request.data.get('phone_number', ''),
            'user_type': 'STAFF'
        }
        
        serializer = UserCreateSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Inactive until admin approval
            user.save()
            
            # Create StaffProfile
            staff_profile = StaffProfile.objects.create(
                user=user,
                employee_id=employee_id,
                role_title=request.data.get('role_title', ''),
                department=request.data.get('department', ''),
                specialization=request.data.get('specialization', ''),
                license_number=request.data.get('license_number', ''),
                license_expiry=request.data.get('license_expiry') or None,
                hire_date=request.data.get('hire_date') or None,
                mfa_enabled=bool(request.data.get('mfa_enabled', False)),
                is_approved=False
            )
            
            return Response({
                'success': True,
                'message': 'Registration submitted successfully. Your account is pending admin approval.',
                'employee_id': employee_id
            }, status=status.HTTP_201_CREATED)
        else:
            errors = {}
            for field, error_list in serializer.errors.items():
                if isinstance(error_list, list):
                    errors[field] = error_list[0] if error_list else 'Invalid value'
                else:
                    errors[field] = str(error_list)
            
            return Response({
                'success': False,
                'errors': errors,
                'error': 'Registration failed. Please check your information.'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.error(f"Staff registration error: {e}", exc_info=True)
        return Response({
            'success': False,
            'error': 'Registration failed. Please try again later.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


