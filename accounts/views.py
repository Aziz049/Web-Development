"""
Views for accounts app
"""
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import timedelta
import json
import hashlib
from .models import (
    DoctorProfile, Branch, DoctorSchedule, PatientProfile, StaffProfile, 
    StaffAuthorizationAttempt, RegistrationAttempt
)
from .serializers import (
    UserSerializer, DoctorProfileSerializer, DoctorProfileCreateSerializer,
    BranchSerializer, DoctorScheduleSerializer, UserCreateSerializer
)

User = get_user_model()


# REFACTOR: Template views for patient/staff registration flows
def access_view(request):
    """Unified entry point for registration - role selection"""
    return render(request, 'access.html')


def patient_register_view(request):
    """
    REFACTOR: Patient registration multi-section form
    HTML-based form that submits silently via fetch() to API
    Patients never see API URLs or DRF pages
    """
    return render(request, 'patient_register.html')


def staff_authorize_view(request):
    """
    REFACTOR: Staff authorization gate - employee ID and registration code
    Prevents unauthorized staff registrations with IP tracking and CAPTCHA
    """
    return render(request, 'staff_authorize.html')


def staff_register_view(request):
    """
    REFACTOR: Staff registration form (after authorization)
    Secure, admin-approved staff onboarding with email domain validation
    """
    # Check if authorization session exists
    if 'staff_authorized' not in request.session:
        return render(request, 'staff_authorize.html', {
            'error': 'Please complete authorization first.'
        })
    return render(request, 'staff_register.html')


# ============================================================================
# REFACTOR: API endpoints for registration
# These endpoints are called via fetch() from HTML forms
# Patients never see these URLs directly - all errors are user-friendly
# ============================================================================

@csrf_exempt
@require_http_methods(["POST"])
def staff_authorize_api(request):
    """
    Staff authorization API endpoint
    Validates employee ID and registration code with IP tracking
    """
    try:
        data = json.loads(request.body)
        employee_id = data.get('employee_id', '').strip()
        registration_code = data.get('registration_code', '').strip()
        
        # Get client IP
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
        if not ip_address:
            ip_address = request.META.get('REMOTE_ADDR', '')
        
        # Check if IP is locked
        cache_key = f'staff_auth_locked_{ip_address}'
        if cache.get(cache_key):
            return JsonResponse({
                'error': 'Too many failed attempts. Please try again in 15 minutes.'
            }, status=429)
        
        # Get recent attempts for this IP
        recent_attempts = StaffAuthorizationAttempt.objects.filter(
            ip_address=ip_address,
            created_at__gte=timezone.now() - timedelta(minutes=15)
        ).order_by('-created_at')
        
        failed_count = recent_attempts.filter(success=False).count()
        
        # Lock after 5 failed attempts
        if failed_count >= 5:
            cache.set(cache_key, True, 900)  # 15 minutes
            return JsonResponse({
                'error': 'Too many failed attempts. Please try again in 15 minutes.'
            }, status=429)
        
        # Validate credentials (in production, check against database)
        # For now, using placeholder validation
        valid_employee_ids = ['EMP001', 'EMP002', 'EMP003']  # Replace with actual validation
        valid_registration_code = 'APEX2024'  # Replace with actual validation
        
        is_valid = (
            employee_id in valid_employee_ids and
            registration_code == valid_registration_code
        )
        
        # Record attempt
        attempt = StaffAuthorizationAttempt.objects.create(
            ip_address=ip_address,
            employee_id=employee_id,
            registration_code=registration_code,
            success=is_valid,
            attempt_count=failed_count + 1
        )
        
        if is_valid:
            # Store in session for registration
            request.session['staff_authorized'] = True
            request.session['staff_employee_id'] = employee_id
            request.session['staff_authorized_at'] = timezone.now().isoformat()
            
            return JsonResponse({
                'success': True,
                'message': 'Authorization successful. Proceeding to registration...'
            })
        else:
            # Check if CAPTCHA needed (after 2 failures)
            needs_captcha = failed_count >= 2
            
            return JsonResponse({
                'error': 'Invalid employee ID or registration code.',
                'needs_captcha': needs_captcha,
                'attempts_remaining': 5 - failed_count - 1
            }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'error': 'An error occurred during authorization.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def patient_register_api(request):
    """
    Patient registration API endpoint
    Creates user with PATIENT role and PatientProfile
    Uses PatientRegistrationSerializer for comprehensive validation
    """
    try:
        data = json.loads(request.body)
        
        # Map re_password to password2 for serializer
        if 're_password' in data:
            data['password2'] = data.pop('re_password')
        
        # Use dedicated PatientRegistrationSerializer
        from .serializers import PatientRegistrationSerializer
        serializer = PatientRegistrationSerializer(data=data)
        
        if serializer.is_valid():
            # Create user and patient profile
            result = serializer.save()
            user = result['user']
            patient_profile = result['patient_profile']
            
            # Track successful registration attempt
            ip_address = request.META.get('REMOTE_ADDR')
            try:
                RegistrationAttempt.objects.create(
                    ip_address=ip_address,
                    user_type='PATIENT',
                    email=user.email,
                    success=True
                )
            except Exception:
                pass  # Don't fail if tracking fails
            
            # Generate JWT tokens for auto-login
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Serialize user data
            from .serializers import UserSerializer
            user_serializer = UserSerializer(user)
            
            return JsonResponse({
                'success': True,
                'message': f'Registration successful! Your Patient ID is: {patient_profile.patient_id}',
                'access': access_token,
                'refresh': refresh_token,
                'user': user_serializer.data,
                'patient_id': patient_profile.patient_id,
                'patient_profile': {
                    'patient_id': patient_profile.patient_id,
                    'date_of_birth': patient_profile.date_of_birth.isoformat() if patient_profile.date_of_birth else None,
                    'gender': patient_profile.gender,
                }
            }, status=201)
        else:
            # Return field-specific errors
            errors = {}
            for field, error_list in serializer.errors.items():
                if isinstance(error_list, list):
                    errors[field] = error_list[0] if error_list else 'Invalid value'
                else:
                    errors[field] = str(error_list)
            
            return JsonResponse({
                'errors': errors,
                'error': 'Please correct the errors below and try again.'
            }, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid request format. Please try again.',
            'errors': {}
        }, status=400)
    except Exception as e:
        # Log the actual error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Patient registration error: {e}", exc_info=True)
        
        # Track failed registration attempt
        ip_address = request.META.get('REMOTE_ADDR')
        try:
            RegistrationAttempt.objects.create(
                ip_address=ip_address,
                user_type='PATIENT',
                email=data.get('email', '') if 'data' in locals() else '',
                success=False,
                error_message=str(e)
            )
        except Exception:
            pass  # Don't fail if tracking fails
        
        # Return detailed error message
        error_msg = f'Registration failed: {str(e)}'
        error_str = str(e).lower()
        if 'email' in error_str or 'already exists' in error_str:
            error_msg = 'This email is already registered. Please use a different email or try logging in.'
        elif 'password' in error_str:
            error_msg = 'Password validation failed. Please ensure your password meets the requirements.'
        elif 'user_type' in error_str or 'column' in error_str:
            error_msg = 'Database error. Please ensure migrations are applied. Run: python manage.py migrate'
        elif 'is_staff' in error_str:
            error_msg = 'Registration error. Please contact support if this persists.'
        
        return JsonResponse({
            'error': error_msg,
            'errors': {},
            'debug': str(e) if settings.DEBUG else None
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def staff_register_api(request):
    """
    Staff registration API endpoint
    Creates user with staff role and StaffProfile (inactive, needs approval)
    """
    # Check authorization
    if 'staff_authorized' not in request.session:
        return JsonResponse({
            'error': 'Authorization required. Please complete authorization first.'
        }, status=403)
    
    try:
        data = json.loads(request.body)
        employee_id = request.session.get('staff_employee_id')
        
        # Validate email domain
        email = data.get('email', '')
        if not email.endswith('@apexdental.com'):  # Replace with actual domain
            return JsonResponse({
                'error': 'Invalid email domain. Staff must use clinic email address.'
            }, status=400)
        
        # Validate password strength (12+ chars for staff)
        password = data.get('password', '')
        if len(password) < 12:
            return JsonResponse({
                'error': 'Password must be at least 12 characters long for staff accounts.'
            }, status=400)
        
        # Validate password match
        if password != data.get('re_password', ''):
            return JsonResponse({
                'error': 'Passwords do not match.'
            }, status=400)
        
        # All staff use STAFF user_type
        user_type = 'STAFF'
        
        # Create user using Djoser serializer directly
        
        user_data = {
            'username': data['username'],
            'email': email,
            'password': password,
            'password_retype': data.get('re_password', ''),
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'phone_number': data.get('phone_number', ''),
            'user_type': user_type
        }
        
        # Use serializer to create user
        serializer = UserCreateSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Inactive until admin approval
            user.save()
            
            # Create StaffProfile
            staff_profile = StaffProfile.objects.create(
                user=user,
                employee_id=employee_id,
                role_title=data.get('role_title', ''),
                department=data.get('department', ''),
                specialization=data.get('specialization', ''),
                license_number=data.get('license_number', ''),
                license_expiry=data.get('license_expiry') or None,
                hire_date=data.get('hire_date') or None,
                mfa_enabled=bool(data.get('mfa_enabled', False)),
                is_approved=False  # Needs admin approval
            )
            
            # Clear session
            request.session.pop('staff_authorized', None)
            request.session.pop('staff_employee_id', None)
            
            # TODO: Notify admin of pending approval
            
            return JsonResponse({
                'success': True,
                'message': 'Registration submitted successfully. Your account is pending admin approval.',
                'employee_id': employee_id
            })
        else:
            error_message = 'Registration failed. '
            errors = []
            for key, value in serializer.errors.items():
                if isinstance(value, list):
                    errors.extend([f"{key}: {v}" for v in value])
                else:
                    errors.append(f"{key}: {value}")
            error_message += ' '.join(errors)
            
            return JsonResponse({
                'error': error_message
            }, status=400)
    
    except User.DoesNotExist:
        return JsonResponse({
            'error': 'User creation failed.'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'error': f'An error occurred: {str(e)}'
        }, status=500)


# ============================================================================
# REFACTOR: Keep existing ViewSets for API (used by frontend JavaScript)
# These are still needed for the appointments/doctors pages
# But patients never navigate to /api/ URLs directly
# ============================================================================

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing users (doctors list for patients)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        queryset = super().get_queryset()
        
        # Patients can only see staff (doctors)
        if self.request.user.is_patient():
            queryset = queryset.filter(user_type='STAFF', is_active=True)
        
        # Staff can see all active users
        elif self.request.user.is_staff():
            queryset = queryset.filter(is_active=True)
        
        # Superusers can see all users
        elif self.request.user.is_superuser:
            queryset = queryset.all()
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def doctors(self, request):
        """Get list of all staff (doctors) with their profiles"""
        doctors = User.objects.filter(user_type='STAFF', is_active=True)
        serializer = self.get_serializer(doctors, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class DoctorProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing doctor profiles
    """
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create' or self.action == 'update':
            return DoctorProfileCreateSerializer
        return DoctorProfileSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        queryset = super().get_queryset()
        
        # Patients can see all doctor profiles
        if self.request.user.is_patient():
            queryset = queryset.filter(user__is_active=True, is_available=True)
        
        # Staff can see their own profile
        elif self.request.user.is_staff():
            queryset = queryset.filter(user=self.request.user)
        
        # Superusers can see all profiles
        elif self.request.user.is_superuser:
            queryset = queryset.all()
        
        return queryset
    
    def perform_create(self, serializer):
        """Create doctor profile for current user"""
        serializer.save(user=self.request.user)


class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing clinic branches
    """
    queryset = Branch.objects.filter(is_active=True)
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def doctors(self, request, pk=None):
        """Get all doctors in a specific branch"""
        branch = self.get_object()
        doctors = User.objects.filter(
            user_type='STAFF',
            is_active=True,
            doctor_profile__branch=branch,
            doctor_profile__is_available=True
        )
        serializer = UserSerializer(doctors, many=True)
        return Response(serializer.data)


class DoctorScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing doctor schedules
    Only doctors can manage their own schedules
    """
    serializer_class = DoctorScheduleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter schedules based on user role"""
        user = self.request.user
        
        if user.is_staff():
            # Staff can only see their own schedules
            if hasattr(user, 'doctor_profile'):
                return DoctorSchedule.objects.filter(doctor=user.doctor_profile)
            return DoctorSchedule.objects.none()
        elif user.is_superuser:
            # Superusers can see all schedules
            return DoctorSchedule.objects.all()
        else:
            # Patients can see schedules for available doctors
            return DoctorSchedule.objects.filter(
                doctor__is_available=True,
                is_available=True
            )
    
    def perform_create(self, serializer):
        """Create schedule for current doctor"""
        user = self.request.user
        
        if not user.is_staff():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only staff can create schedules.")
        
        if not hasattr(user, 'doctor_profile'):
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Doctor profile not found. Please create a doctor profile first.")
        
        serializer.save(doctor=user.doctor_profile)
    
    def perform_update(self, serializer):
        """Update schedule - only the doctor can update their own"""
        user = self.request.user
        schedule = self.get_object()
        
        if not user.is_staff() or schedule.doctor.user != user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only update your own schedules.")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Delete schedule - only the doctor can delete their own"""
        user = self.request.user
        
        if not user.is_staff() or instance.doctor.user != user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own schedules.")
        
        instance.delete()


# ============================================================================
# REFACTOR: Template views (keep existing for backward compatibility)
# ============================================================================

def login_view(request):
    """Render login page"""
    return render(request, 'login.html')


def register_view(request):
    """
    REFACTOR: Old register view - redirects to unified /access/ page
    This ensures /register/ or /access/ is the ONLY registration entry point
    """
    from django.shortcuts import redirect
    return redirect('/access/')


def doctors_view(request):
    """Render doctors list page"""
    return render(request, 'doctors.html')


def appointments_view(request):
    """Render appointments page"""
    return render(request, 'appointments.html')


def index_view(request):
    """Render home page"""
    return render(request, 'index.html')
