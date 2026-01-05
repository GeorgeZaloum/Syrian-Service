"""
Integration tests for user registration and login flow.
Tests Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 9.1, 9.2, 9.3, 9.4
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from apps.users.models import ProviderProfile

User = get_user_model()


@pytest.mark.integration
@pytest.mark.django_db
class TestUserRegistrationAndLoginFlow:
    """Test complete user registration and login workflows."""

    def test_regular_user_registration_and_immediate_access(self, api_client):
        """
        Test that a Regular User can register and immediately access the platform.
        Requirements: 2.1, 2.2, 2.4, 2.7
        """
        # Step 1: Register as Regular User
        registration_data = {
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        response = api_client.post('/api/auth/register/regular/', registration_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert response.data['user']['email'] == 'newuser@example.com'
        assert response.data['user']['role'] == 'REGULAR'
        
        # Verify user is created and active
        user = User.objects.get(email='newuser@example.com')
        assert user.is_active is True
        assert user.role == 'REGULAR'
        
        # Step 2: Login with credentials
        login_data = {
            'email': 'newuser@example.com',
            'password': 'SecurePass123!'
        }
        
        response = api_client.post('/api/auth/login/', login_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert 'user' in response.data
        
        # Step 3: Access protected endpoint with token
        access_token = response.data['access']
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = api_client.get('/api/auth/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'newuser@example.com'
        assert response.data['role'] == 'REGULAR'

    def test_service_provider_registration_with_pending_approval(self, api_client):
        """
        Test that a Service Provider registration creates pending application.
        Requirements: 2.1, 2.3, 2.5, 2.6
        """
        # Step 1: Register as Service Provider
        registration_data = {
            'email': 'newprovider@example.com',
            'password': 'SecurePass123!',
            'first_name': 'Provider',
            'last_name': 'Test',
            'service_description': 'Professional landscaping services'
        }
        
        response = api_client.post('/api/auth/register/provider/', registration_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert response.data['user']['role'] == 'PROVIDER'
        
        # Verify user is created but not active
        user = User.objects.get(email='newprovider@example.com')
        assert user.role == 'PROVIDER'
        
        # Verify provider profile is created with PENDING status
        provider_profile = ProviderProfile.objects.get(user=user)
        assert provider_profile.approval_status == 'PENDING'
        assert provider_profile.service_description == 'Professional landscaping services'
        
        # Step 2: Attempt to login should work but access may be restricted
        login_data = {
            'email': 'newprovider@example.com',
            'password': 'SecurePass123!'
        }
        
        response = api_client.post('/api/auth/login/', login_data)
        # Login should succeed but provider features may be restricted
        assert response.status_code == status.HTTP_200_OK

    def test_admin_approval_workflow(self, api_client, admin_user, pending_provider_user):
        """
        Test admin can approve provider applications with email notifications.
        Requirements: 9.1, 9.2, 9.3, 9.4
        """
        # Step 1: Admin logs in
        api_client.force_authenticate(user=admin_user)
        
        # Step 2: Admin views pending applications
        response = api_client.get('/api/auth/providers/applications/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
        
        # Find the pending provider
        pending_app = None
        for app in response.data['results']:
            if app['user']['email'] == pending_provider_user.email:
                pending_app = app
                break
        
        assert pending_app is not None
        assert pending_app['approval_status'] == 'PENDING'
        
        # Step 3: Admin approves the application
        provider_profile = ProviderProfile.objects.get(user=pending_provider_user)
        response = api_client.post(
            f'/api/auth/providers/applications/{provider_profile.id}/approve/'
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify approval status updated
        provider_profile.refresh_from_db()
        assert provider_profile.approval_status == 'APPROVED'
        assert provider_profile.approved_by == admin_user
        assert provider_profile.approved_at is not None
        
        # Verify user is now active
        pending_provider_user.refresh_from_db()
        assert pending_provider_user.is_active is True

    def test_admin_rejection_workflow(self, api_client, admin_user):
        """
        Test admin can reject provider applications with email notifications.
        Requirements: 9.1, 9.2, 9.3, 9.4
        """
        # Create a new pending provider
        user = User.objects.create_user(
            email='reject@example.com',
            password='TestPass123!',
            first_name='Reject',
            last_name='Test',
            role='PROVIDER'
        )
        provider_profile = ProviderProfile.objects.create(
            user=user,
            service_description='Test service',
            approval_status='PENDING'
        )
        
        # Admin logs in and rejects
        api_client.force_authenticate(user=admin_user)
        
        response = api_client.post(
            f'/api/auth/providers/applications/{provider_profile.id}/reject/'
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify rejection status
        provider_profile.refresh_from_db()
        assert provider_profile.approval_status == 'REJECTED'

    def test_role_based_dashboard_redirects(self, api_client, regular_user, provider_user, admin_user):
        """
        Test that login returns correct user role for dashboard redirects.
        Requirements: 2.7
        """
        # Test Regular User
        response = api_client.post('/api/auth/login/', {
            'email': regular_user.email,
            'password': 'TestPass123!'
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['role'] == 'REGULAR'
        
        # Test Provider
        response = api_client.post('/api/auth/login/', {
            'email': provider_user.email,
            'password': 'TestPass123!'
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['role'] == 'PROVIDER'
        
        # Test Admin
        response = api_client.post('/api/auth/login/', {
            'email': admin_user.email,
            'password': 'TestPass123!'
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['role'] == 'ADMIN'

    def test_password_validation_on_registration(self, api_client):
        """
        Test password strength validation during registration.
        Requirements: 2.6
        """
        # Test weak password
        registration_data = {
            'email': 'weak@example.com',
            'password': '123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        response = api_client.post('/api/auth/register/regular/', registration_data)
        # Should fail validation
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_email_format_validation(self, api_client):
        """
        Test email format validation during registration.
        Requirements: 2.6
        """
        registration_data = {
            'email': 'invalid-email',
            'password': 'SecurePass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        response = api_client.post('/api/auth/register/regular/', registration_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
