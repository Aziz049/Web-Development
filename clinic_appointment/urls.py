"""
URL configuration for clinic_appointment project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from accounts.api_views import api_register_patient, api_register_staff

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation (Swagger/OpenAPI)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Authentication (Djoser + JWT)
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    
    # Registration API endpoints (REST API)
    path('api/auth/register/patient/', api_register_patient, name='api_register_patient'),
    path('api/auth/register/staff/', api_register_staff, name='api_register_staff'),
    
    # Appointments API
    path('api/', include('appointments.urls')),
    
    # Accounts (includes HTML registration forms)
    path('', include('accounts.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


