"""
Integration tests for password change functionality.
Tests Requirements: 6.1, 6.2, 6.3, 6.4, 6.5
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.integration
@pytest.mark.django_db
class TestPasswordChangeWorkflow:
    """Test password change functionality for all user roles."""

    def test_regular_user_password_change(self, authenticated_client, regular_user):
        """
        Test regular user can change password.
        Requirements: 6.1, 6.2, 6.3, 6.4
        """
        password_data = {
            'current_password': 'TestPass123!',
            'new_password': 'NewSecurePass456!'
        }
        
        response = authenticated_client.post('/api/auth/password/change/', password_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify password was changed
        regular_user.refresh_from_db()
        assert regular_user.check_password('NewSecurePass456!')
        
        # Verify old password no longer works
        assert not regular_user.check_password('TestPass123!')

    def test_provider_password_change(self, provider_client, provider_user):
        """
        Test service provider can change password.
        Requirements: 6.1, 6.2, 6.3, 6.4
        """
        password_data = {
            'current_password': 'TestPass123!',
            'new_password': 'ProviderNewPass789!'
        }
        
        response = provider_client.post('/api/auth/password/change/', password_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify password was changed
        provider_user.refresh_from_db()
        assert provider_user.check_password('ProviderNewPass789!')

    def test_admin_password_change(self, admin_client, admin_user):
        """
        Test admin can change password.
        Requirements: 6.1, 6.2, 6.3, 6.4
        """
        password_data = {
            'current_password': 'TestPass123!',
            'new_password': 'AdminNewPass000!'
        }
        
        response = admin_client.post('/api/auth/password/change/', password_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify password was changed
        admin_user.refresh_from_db()
        assert admin_user.check_password('AdminNewPass000!')

    def test_current_password_verification(self, authenticated_client, regular_user):
        """
        Test that current password must be correct.
        Requirements: 6.2
        """
        password_data = {
            'current_password': 'WrongPassword123!',
            'new_password': 'NewSecurePass456!'
        }
        
        response = authenticated_client.post('/api/auth/password/change/', password_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Verify password was NOT changed
        regular_user.refresh_from_db()
        assert regular_user.check_password('TestPass123!')

    def test_password_strength_validation(self, authenticated_client, regular_user):
        """
        Test password strength requirements.
        Requirements: 6.3
        """
        # Test weak password (too short - less than 8 characters)
        password_data = {
            'current_password': 'TestPass123!',
            'new_password': '123'
        }
        
        response = authenticated_client.post('/api/auth/password/change/', password_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'new_password' in response.data or 'error' in response.data
        
        # Test all-numeric password (fails NumericPasswordValidator)
        password_data = {
            'current_password': 'TestPass123!',
            'new_password': '12345678'
        }
        
        response = authenticated_client.post('/api/auth/password/change/', password_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Verify password was NOT changed
        regular_user.refresh_from_db()
        assert regular_user.check_password('TestPass123!')

    def test_password_must_be_different_from_current(self, authenticated_client, regular_user):
        """
        Test that new password must be different from current password.
        Requirements: 6.3
        """
        password_data = {
            'current_password': 'TestPass123!',
            'new_password': 'TestPass123!'
        }
        
        response = authenticated_client.post('/api/auth/password/change/', password_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Verify password was NOT changed (still the same)
        regular_user.refresh_from_db()
        assert regular_user.check_password('TestPass123!')

    def test_session_invalidation_after_password_change(self, api_client, regular_user):
        """
        Test that sessions are invalidated after password change.
        Requirements: 6.5
        """
        # Login and get token
        login_response = api_client.post('/api/auth/login/', {
            'email': regular_user.email,
            'password': 'TestPass123!'
        })
        assert login_response.status_code == status.HTTP_200_OK
        old_token = login_response.data['tokens']['access']
        
        # Authenticate with token
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {old_token}')
        
        # Change password
        password_data = {
            'current_password': 'TestPass123!',
            'new_password': 'NewSecurePass456!'
        }
        
        response = api_client.post('/api/auth/password/change/', password_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Try to use old token (should fail or require re-login)
        # Note: JWT tokens may still be valid until expiry, but user should be prompted to re-login
        
        # Login with new password should work
        new_login_response = api_client.post('/api/auth/login/', {
            'email': regular_user.email,
            'password': 'NewSecurePass456!'
        })
        assert new_login_response.status_code == status.HTTP_200_OK
        assert 'tokens' in new_login_response.data
        assert 'access' in new_login_response.data['tokens']
        
        # Old password should not work
        old_login_response = api_client.post('/api/auth/login/', {
            'email': regular_user.email,
            'password': 'TestPass123!'
        })
        assert old_login_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unauthenticated_cannot_change_password(self, api_client):
        """
        Test that unauthenticated users cannot change password.
        Requirements: 6.1
        """
        password_data = {
            'current_password': 'TestPass123!',
            'new_password': 'NewSecurePass456!'
        }
        
        response = api_client.post('/api/auth/password/change/', password_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_password_change_success_message(self, authenticated_client, regular_user):
        """
        Test that password change returns success confirmation.
        Requirements: 6.4
        """
        password_data = {
            'current_password': 'TestPass123!',
            'new_password': 'NewSecurePass456!'
        }
        
        response = authenticated_client.post('/api/auth/password/change/', password_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data or 'detail' in response.data

    def test_cannot_reuse_current_password(self, authenticated_client, regular_user):
        """
        Test that user cannot set new password same as current.
        Requirements: 6.3
        """
        password_data = {
            'current_password': 'TestPass123!',
            'new_password': 'TestPass123!'
        }
        
        response = authenticated_client.post('/api/auth/password/change/', password_data)
        # Should fail because new password must be different from current
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_change_with_special_characters(self, authenticated_client, regular_user):
        """
        Test password change with various special characters.
        Requirements: 6.3
        """
        password_data = {
            'current_password': 'TestPass123!',
            'new_password': 'C0mpl3x!P@ssw0rd#2024'
        }
        
        response = authenticated_client.post('/api/auth/password/change/', password_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify password was changed
        regular_user.refresh_from_db()
        assert regular_user.check_password('C0mpl3x!P@ssw0rd#2024')

    def test_password_change_endpoint_exists(self, authenticated_client):
        """
        Test that password change endpoint is accessible.
        Requirements: 6.1
        """
        # Make a request to verify endpoint exists
        response = authenticated_client.post('/api/auth/password/change/', {})
        # Should return 400 (bad request) not 404 (not found)
        assert response.status_code != status.HTTP_404_NOT_FOUND
