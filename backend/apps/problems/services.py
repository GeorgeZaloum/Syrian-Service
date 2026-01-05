"""
Business logic services for problem reporting.
"""
from typing import Dict, Any
from django.core.files.uploadedfile import UploadedFile
from .models import ProblemReport
from .ai_service import AIRecommendationService
from .transcription_service import VoiceTranscriptionService
import logging

logger = logging.getLogger(__name__)


class ProblemReportService:
    """Service for managing problem reports."""
    
    def __init__(self):
        self.ai_service = AIRecommendationService()
        self.transcription_service = VoiceTranscriptionService()
    
    def create_problem_report(
        self,
        user,
        input_type: str,
        problem_text: str = None,
        audio_file: UploadedFile = None
    ) -> ProblemReport:
        """
        Create a new problem report with AI recommendations.
        
        Args:
            user: The user submitting the report
            input_type: 'TEXT' or 'VOICE'
            problem_text: The problem description (for TEXT type)
            audio_file: The audio file (for VOICE type)
            
        Returns:
            Created ProblemReport instance
            
        Raises:
            ValueError: If validation fails
            Exception: If processing fails
        """
        try:
            # Process based on input type
            if input_type == 'VOICE':
                # Transcribe audio to text
                logger.info(f"Transcribing audio file for user {user.email}")
                problem_text = self.transcription_service.transcribe_audio(audio_file)
                logger.info(f"Transcription successful: {problem_text[:100]}...")
            
            # Generate AI recommendations
            logger.info(f"Generating recommendations for problem: {problem_text[:100]}...")
            recommendations = self.ai_service.generate_recommendations(problem_text)
            logger.info(f"Generated {len(recommendations)} recommendations")
            
            # Create problem report
            problem_report = ProblemReport.objects.create(
                user=user,
                input_type=input_type,
                problem_text=problem_text,
                audio_file=audio_file if input_type == 'VOICE' else None,
                recommendations=recommendations
            )
            
            logger.info(f"Created problem report {problem_report.id} for user {user.email}")
            return problem_report
            
        except ValueError as e:
            # Validation errors
            logger.error(f"Validation error creating problem report: {str(e)}")
            raise
        except Exception as e:
            # Processing errors
            logger.error(f"Error creating problem report: {str(e)}")
            raise Exception(f"Failed to process problem report: {str(e)}")
    
    def get_user_problem_reports(self, user, limit: int = None):
        """
        Get all problem reports for a specific user.
        
        Args:
            user: The user whose reports to retrieve
            limit: Optional limit on number of reports
            
        Returns:
            QuerySet of ProblemReport instances
        """
        queryset = ProblemReport.objects.filter(user=user).order_by('-created_at')
        
        if limit:
            queryset = queryset[:limit]
        
        return queryset
    
    def get_problem_report_by_id(self, report_id: int, user) -> ProblemReport:
        """
        Get a specific problem report by ID.
        
        Args:
            report_id: The problem report ID
            user: The user requesting the report
            
        Returns:
            ProblemReport instance
            
        Raises:
            ProblemReport.DoesNotExist: If report not found or user doesn't have access
        """
        try:
            # Ensure user can only access their own reports
            return ProblemReport.objects.get(id=report_id, user=user)
        except ProblemReport.DoesNotExist:
            logger.warning(f"Problem report {report_id} not found for user {user.email}")
            raise
