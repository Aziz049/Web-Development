"""
ViewSet for Visit History (MongoDB)
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import VisitHistorySerializer
from .mongo import (
    get_visit_history_by_patient,
    get_visit_history_by_doctor,
    get_all_visit_history
)


class VisitHistoryViewSet(viewsets.ViewSet):
    """
    ViewSet for viewing visit history from MongoDB.
    
    Note: This ViewSet doesn't use Django models since visit history
    is stored in MongoDB. It uses custom MongoDB operations.
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """
        Get visit history based on user role:
        - Patients: see only their own history
        - Doctors: see history for their patients
        - Admins: see all records
        """
        user = request.user
        
        try:
            if user.is_patient():
                # Patients see only their own visit history
                records = get_visit_history_by_patient(user.id)
            
            elif user.is_staff():
                # Staff see visit history for their patients
                records = get_visit_history_by_doctor(user.id)
            
            elif user.is_superuser:
                # Superusers see all visit history
                records = get_all_visit_history()
            
            else:
                return Response(
                    {"error": "Invalid user role."},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Serialize the MongoDB documents
            serializer = VisitHistorySerializer(records, many=True)
            return Response(serializer.data)
        
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve visit history: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

