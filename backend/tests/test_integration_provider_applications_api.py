"""
Integration tests for provider applications API endpoint.
Tests Requirements: 1.4, 2.1
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.users.models import ProviderProfile

User = get_user_model()


@pytest.mark.integration
@pytest.mark.django_db
class TestProviderApplicationsAPI:
    """Test /api/providers/applications/ endpoint."""

    def test_endpoint_returns_applications_with_user_details_field(self, admin_client, pending_provider_user):
        """
        Test that the endpoint returns applications with user_details field.
        Requirements: 1.4
        """
        response = admin_client.get('/api/auth/providers/applications/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) > 0
        
        # Check that each application has user_details field
        for application in response.data['results']:
            assert 'user_details' in application
            assert application['user_details'] is not None
            
            # Verify user_details structure
            user_details = application['user_details']
            assert 'id' in user_details
            assert 'email' in user_details
            assert 'first_name' in user_details
            assert 'last_name' in user_details
            assert 'role' in user_details
            assert 'is_active' in user_details
            assert 'created_at' in user_details

    def test_endpoint_does_not_return_user_field(self, admin_client, pending_provider_user):
        """
        Test that the endpoint does not return 'user' field (only 'user_details').
        Requirements: 1.4
        """
        response = admin_client.get('/api/auth/providers/applications/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        
        # Check that 'user' field is not present
        for application in response.data['results']:
            assert 'user' not in application
            assert 'user_details' in application

    def test_endpoint_returns_only_pending_applications(self, admin_client, db):
        """
        Test that only PENDING applications are returned.
        Requirements: 1.4, 2.1
        """
        # Create providers with different statuses
        pending_user = User.objects.create_user(
            email='pending1@example.com',
            password='TestPass123!',
            first_name='Pending',
            last_name='Provider',
            role='PROVIDER',
            is_active=False
        )
        ProviderProfile.objects.create(
            user=pending_user,
            service_description='Pending service',
            approval_status='PENDING'
        )
        
        approved_user = User.objects.create_user(
            email='approved@example.com',
            password='TestPass123!',
            first_name='Approved',
            last_name='Provider',
            role='PROVIDER',
            is_active=True
        )
        ProviderProfile.objects.create(
            user=approved_user,
            service_description='Approved service',
            approval_status='APPROVED'
        )
        
        rejected_user = User.objects.create_user(
            email='rejected@example.com',
            password='TestPass123!',
            first_name='Rejected',
            last_name='Provider',
            role='PROVIDER',
            is_active=False
        )
        ProviderProfile.objects.create(
            user=rejected_user,
            service_description='Rejected service',
            approval_status='REJECTED'
        )
        
        response = admin_client.get('/api/auth/providers/applications/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        
        # Verify only PENDING applications are returned
        for application in response.data['results']:
            assert application['approval_status'] == 'PENDING'
        
        # Verify count matches pending applications
        pending_count = ProviderProfile.objects.filter(approval_status='PENDING').count()
        assert response.data['count'] == pending_count

    def test_endpoint_requires_admin_authentication(self, api_client, pending_provider_user):
        """
        Test that admin authentication is required to access the endpoint.
        Requirements: 2.1
        """
        # Test unauthenticated access
        response = api_client.get('/api/auth/providers/applications/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_endpoint_denies_regular_user_access(self, authenticated_client, pending_provider_user):
        """
        Test that regular users cannot access the endpoint.
        Requirements: 2.1
        """
        response = authenticated_client.get('/api/auth/providers/applications/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert 'error' in response.data
        assert response.data['error']['code'] == 'FORBIDDEN'

    def test_endpoint_denies_provider_user_access(self, provider_client, pending_provider_user):
        """
        Test that provider users cannot access the endpoint.
        Requirements: 2.1
        """
        response = provider_client.get('/api/auth/providers/applications/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert 'error' in response.data
        assert response.data['error']['code'] == 'FORBIDDEN'

    def test_endpoint_returns_correct_application_data(self, admin_client, db):
        """
        Test that the endpoint returns complete and correct application data.
        Requirements: 1.4, 2.1
        """
        # Create a test provider application
        test_user = User.objects.create_user(
            email='testprovider@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='Provider',
            role='PROVIDER',
            is_active=False
        )
        test_profile = ProviderProfile.objects.create(
            user=test_user,
            service_description='Professional testing services',
            approval_status='PENDING'
        )
        
        response = admin_client.get('/api/auth/providers/applications/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        
        # Find the test application in results
        test_application = None
        for app in response.data['results']:
            if app['id'] == test_profile.id:
                test_application = app
                break
        
        assert test_application is not None
        
        # Verify application fields
        assert test_application['service_description'] == 'Professional testing services'
        assert test_application['approval_status'] == 'PENDING'
        
        # Verify user_details fields
        user_details = test_application['user_details']
        assert user_details['email'] == 'testprovider@example.com'
        assert user_details['first_name'] == 'Test'
        assert user_details['last_name'] == 'Provider'
        assert user_details['role'] == 'PROVIDER'
        assert user_details['is_active'] is False

    def test_endpoint_returns_empty_list_when_no_pending_applications(self, admin_client, db):
        """
        Test that the endpoint returns an empty list when no pending applications exist.
        Requirements: 2.1
        """
        # Ensure no pending applications exist
        ProviderProfile.objects.filter(approval_status='PENDING').delete()
        
        response = admin_client.get('/api/auth/providers/applications/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert response.data['count'] == 0
        assert len(response.data['results']) == 0

    def test_endpoint_with_multiple_pending_applications(self, admin_client, db):
        """
        Test that the endpoint returns all pending applications.
        Requirements: 1.4, 2.1
        """
        # Create multiple pending applications
        for i in range(3):
            user = User.objects.create_user(
                email=f'provider{i}@example.com',
                password='TestPass123!',
                first_name=f'Provider{i}',
                last_name='Test',
                role='PROVIDER',
                is_active=False
            )
            ProviderProfile.objects.create(
                user=user,
                service_description=f'Service description {i}',
                approval_status='PENDING'
            )
        
        response = admin_client.get('/api/auth/providers/applications/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        
        # Verify all pending applications are returned
        pending_count = ProviderProfile.objects.filter(approval_status='PENDING').count()
        assert response.data['count'] == pending_count
        assert len(response.data['results']) == pending_count
        
        # Verify each has user_details
        for application in response.data['results']:
            assert 'user_details' in application
            assert application['approval_status'] == 'PENDING'
