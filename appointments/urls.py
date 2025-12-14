"""
URLs for appointments app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet
from .visit_history_views import VisitHistoryViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'visit-history', VisitHistoryViewSet, basename='visit-history')

urlpatterns = [
    path('', include(router.urls)),
]


