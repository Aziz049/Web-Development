"""
URLs for accounts app
REFACTOR: Updated to use /access/ as unified entry point
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, DoctorProfileViewSet, BranchViewSet, DoctorScheduleViewSet,
    login_view, register_view, doctors_view, 
    appointments_view, index_view,
    access_view, patient_register_view, staff_authorize_view, staff_register_view,
    patient_register_api, staff_authorize_api, staff_register_api
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'doctors', DoctorProfileViewSet, basename='doctor-profile')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'schedules', DoctorScheduleViewSet, basename='doctor-schedule')

urlpatterns = [
    # API routes (internal use only - not exposed to patients)
    path('api/', include(router.urls)),
    
    # REFACTOR: Unified access point
    path('access/', access_view, name='access'),
    
    # REFACTOR: Patient registration flow
    path('access/patient/', patient_register_view, name='patient_register'),
    path('api/register/patient/', patient_register_api, name='patient_register_api'),
    
    # REFACTOR: Staff authorization and registration flow
    path('access/staff/authorize/', staff_authorize_view, name='staff_authorize'),
    path('access/staff/register/', staff_register_view, name='staff_register'),
    path('api/staff/authorize/', staff_authorize_api, name='staff_authorize_api'),
    path('api/staff/register/', staff_register_api, name='staff_register_api'),
    
    # Frontend routes
    path('', index_view, name='index'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),  # Redirects to /access/
    path('doctors/', doctors_view, name='doctors'),
    path('appointments/', appointments_view, name='appointments'),
]

