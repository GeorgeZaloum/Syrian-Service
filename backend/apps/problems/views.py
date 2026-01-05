"""
API views for problem reporting.
"""
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import ProblemReport
from .serializers import (
    ProblemReportCreateSerializer,
    ProblemReportSerializer,
    ProblemReportListSerializer
)
from .services import ProblemReportService
import logging

logger = logging.getLogger(__name__)


class ProblemReportCreateView(generics.CreateAPIView):
    """
    API endpoint for creating problem reports.
    
    POST /api/problems/
    - Accepts text or voice input
    - Generates AI recommendations
    - Returns problem report with recommendations
    """
    serializer_class = ProblemReportCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def create(self, request, *args, **kwargs):
        """Handle problem report creation."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Extract validated data
            input_type = serializer.validated_data.get('input_type')
            problem_text = serializer.validated_data.get('problem_text')
            audio_file = serializer.validated_data.get('audio_file')
            
            # Create problem report using service
            service = ProblemReportService()
            problem_report = service.create_problem_report(
                user=request.user,
                input_type=input_type,
                problem_text=problem_text,
                audio_file=audio_file
            )
            
            # Serialize and return response
            response_serializer = ProblemReportSerializer(problem_report)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except ValueError as e:
            # Validation errors
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Processing errors
            logger.error(f"Error creating problem report: {str(e)}")
            return Response(
                {'error': 'Failed to process problem report. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProblemReportListView(generics.ListAPIView):
    """
    API endpoint for listing user's problem reports.
    
    GET /api/problems/
    - Returns all problem reports for the authenticated user
    - Ordered by creation date (newest first)
    """
    serializer_class = ProblemReportListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return problem reports for the authenticated user only."""
        service = ProblemReportService()
        return service.get_user_problem_reports(self.request.user)


class ProblemReportDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a specific problem report.
    
    GET /api/problems/{id}/
    - Returns detailed problem report with recommendations
    - Users can only access their own reports
    """
    serializer_class = ProblemReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Get problem report ensuring user has access."""
        report_id = self.kwargs.get('pk')
        service = ProblemReportService()
        
        try:
            return service.get_problem_report_by_id(report_id, self.request.user)
        except ProblemReport.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound('Problem report not found or you do not have access to it.')
