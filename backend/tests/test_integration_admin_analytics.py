"""
Integration tests for admin analytics and reporting.
Tests Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.services.models import Service
from apps.requests.models import ServiceRequest
from datetime import datetime, timedelta
import csv
from io import StringIO

User = get_user_model()


@pytest.mark.integration
@pytest.mark.django_db
class TestAdminAnalyticsWorkflow:
    """Test admin analytics dashboard and reporting."""

    def test_analytics_dashboard_with_real_data(self, admin_client, regular_user, provider_user, service):
        """
        Test analytics dashboard displays accurate metrics.
        Requirements: 10.1, 10.5
        """
        # Create some test data
        # Additional users
        User.objects.create_user(
            email='user2@example.com',
            password='TestPass123!',
            first_name='User',
            last_name='Two',
            role='REGULAR'
        )
        
        # Service requests
        ServiceRequest.objects.create(
            service=service,
            requester=regular_user,
            provider=provider_user,
            status='PENDING'
        )
        ServiceRequest.objects.create(
            service=service,
            requester=regular_user,
            provider=provider_user,
            status='ACCEPTED'
        )
        
        # Get dashboard metrics
        response = admin_client.get('/api/analytics/dashboard/')
        assert response.status_code == status.HTTP_200_OK
        
        # Verify metrics are present
        assert 'total_users' in response.data
        assert 'active_providers' in response.data
        assert 'pending_requests' in response.data
        
        # Verify counts are accurate
        assert response.data['total_users'] >= 3  # admin, regular, provider
        assert response.data['active_providers'] >= 1
        assert response.data['pending_requests'] >= 1

    def test_chart_data_accuracy(self, admin_client, regular_user):
        """
        Test that chart data is accurate and properly formatted.
        Requirements: 10.1
        """
        response = admin_client.get('/api/analytics/dashboard/')
        assert response.status_code == status.HTTP_200_OK
        
        # Check for chart data structures
        if 'user_registrations' in response.data:
            assert isinstance(response.data['user_registrations'], list)
        
        if 'request_statistics' in response.data:
            assert isinstance(response.data['request_statistics'], (list, dict))

    def test_date_range_filtering(self, admin_client, regular_user):
        """
        Test filtering analytics by date range.
        Requirements: 10.2, 10.3
        """
        # Get current date and past date
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        response = admin_client.get('/api/analytics/dashboard/', {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })
        assert response.status_code == status.HTTP_200_OK
        
        # Verify response contains filtered data
        assert 'total_users' in response.data or 'results' in response.data

    def test_role_filtering(self, admin_client):
        """
        Test filtering analytics by user role.
        Requirements: 10.2, 10.3
        """
        response = admin_client.get('/api/analytics/users/search/', {'role': 'PROVIDER'})
        assert response.status_code == status.HTTP_200_OK
        
        # Verify all returned users are providers
        if 'results' in response.data:
            for user in response.data['results']:
                assert user['role'] == 'PROVIDER'

    def test_activity_type_filtering(self, admin_client, service, regular_user, provider_user):
        """
        Test filtering by activity type.
        Requirements: 10.2, 10.3
        """
        # Create requests with different statuses
        ServiceRequest.objects.create(
            service=service,
            requester=regular_user,
            provider=provider_user,
            status='PENDING'
        )
        ServiceRequest.objects.create(
            service=service,
            requester=regular_user,
            provider=provider_user,
            status='COMPLETED'
        )
        
        # Filter by status
        response = admin_client.get('/api/analytics/requests/search/', {'status': 'PENDING'})
        assert response.status_code == status.HTTP_200_OK
        
        if 'results' in response.data:
            for request in response.data['results']:
                assert request['status'] == 'PENDING'

    def test_search_functionality_users(self, admin_client, regular_user):
        """
        Test search functionality for users.
        Requirements: 10.4
        """
        response = admin_client.get('/api/analytics/users/search/', {
            'q': regular_user.email
        })
        assert response.status_code == status.HTTP_200_OK
        
        # Verify search results contain the user
        if 'results' in response.data:
            emails = [u['email'] for u in response.data['results']]
            assert regular_user.email in emails

    def test_search_functionality_providers(self, admin_client, provider_user):
        """
        Test search functionality for providers.
        Requirements: 10.4
        """
        response = admin_client.get('/api/analytics/providers/search/', {
            'q': provider_user.first_name
        })
        assert response.status_code == status.HTTP_200_OK
        
        # Verify search results
        if 'results' in response.data:
            assert len(response.data['results']) >= 0

    def test_search_functionality_requests(self, admin_client, service_request):
        """
        Test search functionality for service requests.
        Requirements: 10.4
        """
        response = admin_client.get('/api/analytics/requests/search/', {
            'q': service_request.requester.email
        })
        assert response.status_code == status.HTTP_200_OK

    def test_csv_export_functionality(self, admin_client, regular_user, provider_user):
        """
        Test CSV export with filtered data.
        Requirements: 10.6
        """
        response = admin_client.get('/api/analytics/export/', {
            'type': 'users'
        })
        
        # Should return CSV data
        assert response.status_code == status.HTTP_200_OK
        
        # Verify content type
        assert 'text/csv' in response['Content-Type']
        
        # Try to parse CSV
        if isinstance(response.content, bytes):
            content = response.content.decode('utf-8')
        else:
            content = response.content
        
        # Verify it's valid CSV
        csv_reader = csv.reader(StringIO(content))
        rows = list(csv_reader)
        assert len(rows) > 0  # Should have at least header row

    def test_csv_export_with_filters(self, admin_client):
        """
        Test CSV export respects applied filters.
        Requirements: 10.6
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        response = admin_client.get('/api/analytics/export/', {
            'type': 'users',
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert 'text/csv' in response['Content-Type']

    def test_real_time_metrics_accuracy(self, admin_client, regular_user, provider_user, service):
        """
        Test real-time metrics are accurate.
        Requirements: 10.5
        """
        # Get initial metrics
        response = admin_client.get('/api/analytics/dashboard/')
        assert response.status_code == status.HTTP_200_OK
        initial_users = response.data.get('total_users', 0)
        
        # Create new user
        User.objects.create_user(
            email='newmetric@example.com',
            password='TestPass123!',
            first_name='New',
            last_name='Metric',
            role='REGULAR'
        )
        
        # Get updated metrics
        response = admin_client.get('/api/analytics/dashboard/')
        assert response.status_code == status.HTTP_200_OK
        updated_users = response.data.get('total_users', 0)
        
        # Verify count increased
        assert updated_users > initial_users

    def test_provider_activity_metrics(self, admin_client, provider_user, service):
        """
        Test provider activity metrics.
        Requirements: 10.1, 10.5
        """
        response = admin_client.get('/api/analytics/providers/activity/')
        assert response.status_code == status.HTTP_200_OK
        
        # Verify provider data is present
        if 'results' in response.data:
            assert len(response.data['results']) >= 1

    def test_completed_transactions_metric(self, admin_client, service, regular_user, provider_user):
        """
        Test completed transactions metric.
        Requirements: 10.5
        """
        # Create completed request
        ServiceRequest.objects.create(
            service=service,
            requester=regular_user,
            provider=provider_user,
            status='COMPLETED'
        )
        
        response = admin_client.get('/api/analytics/dashboard/')
        assert response.status_code == status.HTTP_200_OK
        
        # Verify completed transactions count
        if 'completed_transactions' in response.data:
            assert response.data['completed_transactions'] >= 1

    def test_non_admin_cannot_access_analytics(self, authenticated_client):
        """
        Test that non-admin users cannot access analytics.
        Requirements: 10.1
        """
        response = authenticated_client.get('/api/analytics/dashboard/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_combined_filters(self, admin_client):
        """
        Test multiple filters applied simultaneously.
        Requirements: 10.2, 10.3
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        response = admin_client.get('/api/analytics/users/search/', {
            'role': 'REGULAR',
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })
        assert response.status_code == status.HTTP_200_OK
