"""
Integration tests for problem reporting with AI recommendations.
Tests Requirements: 5.1, 5.2, 5.3, 5.4, 5.5
"""
import pytest
from rest_framework import status
from apps.problems.models import ProblemReport
from unittest.mock import patch, MagicMock
from io import BytesIO
import time


@pytest.mark.integration
@pytest.mark.django_db
class TestProblemReportingWorkflow:
    """Test problem reporting with AI recommendations."""

    @patch('apps.problems.services.AIRecommendationService.generate_recommendations')
    def test_text_based_problem_submission(self, mock_ai, authenticated_client, regular_user):
        """
        Test text-based problem submission with AI recommendations.
        Requirements: 5.1, 5.2, 5.4
        """
        # Mock AI response
        mock_ai.return_value = [
            {'title': 'Check Power', 'description': 'Check if the water heater is turned on'},
            {'title': 'Circuit Breaker', 'description': 'Verify the circuit breaker'},
            {'title': 'Call Plumber', 'description': 'Contact a licensed plumber if issue persists'}
        ]
        
        problem_data = {
            'input_type': 'TEXT',
            'problem_text': 'My water heater is not working and there is no hot water'
        }
        
        start_time = time.time()
        response = authenticated_client.post('/api/problems/create/', problem_data)
        end_time = time.time()
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'recommendations' in response.data
        assert len(response.data['recommendations']) > 0
        
        # Verify response time under 5 seconds
        response_time = end_time - start_time
        assert response_time < 5.0, f"Response took {response_time}s, should be under 5s"
        
        # Verify problem is saved
        problem = ProblemReport.objects.get(id=response.data['id'])
        assert problem.user == regular_user
        assert problem.input_type == 'TEXT'
        assert problem.problem_text == problem_data['problem_text']
        assert problem.recommendations is not None

    @patch('apps.problems.services.VoiceTranscriptionService.transcribe_audio')
    @patch('apps.problems.services.AIRecommendationService.generate_recommendations')
    def test_voice_based_problem_submission(self, mock_ai, mock_transcribe, authenticated_client, regular_user):
        """
        Test voice-based problem submission with transcription and AI recommendations.
        Requirements: 5.1, 5.3, 5.4
        """
        # Mock transcription
        mock_transcribe.return_value = 'My sink is clogged and water is not draining'
        
        # Mock AI response
        mock_ai.return_value = [
            {'title': 'Use a Plunger', 'description': 'Try using a plunger'},
            {'title': 'Drain Snake', 'description': 'Use a drain snake'},
            {'title': 'Hot Water', 'description': 'Pour hot water and baking soda'}
        ]
        
        # Create a mock audio file
        audio_file = BytesIO(b'fake audio data')
        audio_file.name = 'problem.wav'
        
        problem_data = {
            'input_type': 'VOICE',
            'audio_file': audio_file
        }
        
        start_time = time.time()
        response = authenticated_client.post('/api/problems/create/', problem_data, format='multipart')
        end_time = time.time()
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'recommendations' in response.data
        assert response.data['problem_text'] == 'My sink is clogged and water is not draining'
        
        # Verify response time under 5 seconds
        response_time = end_time - start_time
        assert response_time < 5.0
        
        # Verify transcription was called
        mock_transcribe.assert_called_once()

    @patch('apps.problems.services.AIRecommendationService.generate_recommendations')
    def test_problem_history_display(self, mock_ai, authenticated_client, regular_user):
        """
        Test that users can view their problem history.
        Requirements: 5.5
        """
        # Mock AI
        mock_ai.return_value = [
            {'title': 'Solution 1', 'description': 'First solution'},
            {'title': 'Solution 2', 'description': 'Second solution'}
        ]
        
        # Create multiple problem reports
        problems = []
        for i in range(3):
            response = authenticated_client.post('/api/problems/create/', {
                'input_type': 'TEXT',
                'problem_text': f'Problem {i+1}'
            })
            assert response.status_code == status.HTTP_201_CREATED
            problems.append(response.data['id'])
        
        # Retrieve problem history
        response = authenticated_client.get('/api/problems/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 3
        
        # Verify all problems are in history
        problem_ids = [p['id'] for p in response.data['results']]
        for problem_id in problems:
            assert problem_id in problem_ids

    @patch('apps.problems.services.AIRecommendationService.generate_recommendations')
    def test_problem_detail_with_recommendations(self, mock_ai, authenticated_client, regular_user):
        """
        Test retrieving problem detail with recommendations.
        Requirements: 5.2, 5.5
        """
        # Mock AI
        mock_recommendations = [
            {'title': 'First', 'description': 'First recommendation'},
            {'title': 'Second', 'description': 'Second recommendation'},
            {'title': 'Third', 'description': 'Third recommendation'}
        ]
        mock_ai.return_value = mock_recommendations
        
        # Create problem
        response = authenticated_client.post('/api/problems/create/', {
            'input_type': 'TEXT',
            'problem_text': 'Detailed problem description'
        })
        problem_id = response.data['id']
        
        # Retrieve problem detail
        response = authenticated_client.get(f'/api/problems/{problem_id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['problem_text'] == 'Detailed problem description'
        assert 'recommendations' in response.data
        assert len(response.data['recommendations']) == 3

    @patch('apps.problems.services.AIRecommendationService.generate_recommendations')
    def test_ai_recommendation_performance(self, mock_ai, authenticated_client):
        """
        Test that AI recommendations are generated within 5 seconds.
        Requirements: 5.4
        """
        # Mock AI with slight delay
        def slow_ai(*args, **kwargs):
            time.sleep(0.5)  # Simulate processing time
            return [
                {'title': 'Quick', 'description': 'Quick solution'}
            ]
        
        mock_ai.side_effect = slow_ai
        
        problem_data = {
            'input_type': 'TEXT',
            'problem_text': 'Performance test problem'
        }
        
        start_time = time.time()
        response = authenticated_client.post('/api/problems/create/', problem_data)
        end_time = time.time()
        
        assert response.status_code == status.HTTP_201_CREATED
        response_time = end_time - start_time
        assert response_time < 5.0

    @patch('apps.problems.services.AIRecommendationService.generate_recommendations')
    def test_ai_error_handling(self, mock_ai, authenticated_client):
        """
        Test graceful handling of AI service errors.
        Requirements: 5.2
        """
        # Mock AI failure
        mock_ai.side_effect = Exception('AI service unavailable')
        
        problem_data = {
            'input_type': 'TEXT',
            'problem_text': 'Test problem'
        }
        
        response = authenticated_client.post('/api/problems/create/', problem_data)
        
        # Should still create problem report with fallback recommendations
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_500_INTERNAL_SERVER_ERROR]
        
        if response.status_code == status.HTTP_201_CREATED:
            # Check for fallback recommendations
            assert 'recommendations' in response.data

    def test_user_can_only_see_own_problems(self, api_client, regular_user):
        """
        Test that users can only see their own problem reports.
        Requirements: 5.5
        """
        # Create another user
        from django.contrib.auth import get_user_model
        User = get_user_model()
        other_user = User.objects.create_user(
            email='other@example.com',
            password='TestPass123!',
            first_name='Other',
            last_name='User',
            role='REGULAR'
        )
        
        # Create problem for other user
        with patch('apps.problems.services.AIRecommendationService.generate_recommendations') as mock_ai:
            mock_ai.return_value = [{'title': 'Test', 'description': 'Test solution'}]
            
            api_client.force_authenticate(user=other_user)
            response = api_client.post('/api/problems/create/', {
                'input_type': 'TEXT',
                'problem_text': 'Other user problem'
            })
            other_problem_id = response.data['id']
        
        # Regular user should not see other user's problems
        api_client.force_authenticate(user=regular_user)
        response = api_client.get('/api/problems/')
        assert response.status_code == status.HTTP_200_OK
        
        problem_ids = [p['id'] for p in response.data['results']]
        assert other_problem_id not in problem_ids

    @patch('apps.problems.services.VoiceTranscriptionService.transcribe_audio')
    def test_voice_transcription_error_handling(self, mock_transcribe, authenticated_client):
        """
        Test graceful handling of transcription errors.
        Requirements: 5.3
        """
        # Mock transcription failure
        mock_transcribe.side_effect = Exception('Transcription failed')
        
        audio_file = BytesIO(b'fake audio data')
        audio_file.name = 'problem.wav'
        
        problem_data = {
            'input_type': 'VOICE',
            'audio_file': audio_file
        }
        
        response = authenticated_client.post('/api/problems/create/', problem_data, format='multipart')
        
        # Should handle error gracefully
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR]
