"""
Unit tests for ProviderProfileSerializer.
Tests Requirements: 1.1, 1.2, 1.3
"""
import pytest
from django.contrib.auth import get_user_model
from apps.users.models import ProviderProfile
from apps.users.serializers import ProviderProfileSerializer

User = get_user_model()


@pytest.mark.django_db
class TestProviderProfileSerializer:
    """Test ProviderProfileSerializer output format."""

    def test_serializer_contains_user_details_field(self, db):
        """
        Test that serialized output contains user_details field.
        Requirements: 1.1, 1.2
        """
        # Create user and provider profile
        user = User.objects.create_user(
            email='testprovider@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='Provider',
            role='PROVIDER',
            is_active=False
        )
        provider_profile = ProviderProfile.objects.create(
            user=user,
            service_description='Test service description',
            approval_status='PENDING'
        )
        
        # Serialize the provider profile
        serializer = ProviderProfileSerializer(provider_profile)
        data = serializer.data
        
        # Assert user_details field exists
        assert 'user_details' in data
        assert data['user_details'] is not None

    def test_user_details_contains_required_fields(self, db):
        """
        Test that user_details contains all required user fields.
        Requirements: 1.2, 1.3
        """
        # Create user and provider profile
        user = User.objects.create_user(
            email='provider2@example.com',
            password='TestPass123!',
            first_name='John',
            last_name='Doe',
            role='PROVIDER',
            is_active=False
        )
        provider_profile = ProviderProfile.objects.create(
            user=user,
            service_description='Professional plumbing services',
            approval_status='PENDING'
        )
        
        # Serialize the provider profile
        serializer = ProviderProfileSerializer(provider_profile)
        data = serializer.data
        
        # Assert user_details contains all required fields
        user_details = data['user_details']
        assert 'id' in user_details
        assert 'email' in user_details
        assert 'first_name' in user_details
        assert 'last_name' in user_details
        assert 'role' in user_details
        assert 'is_active' in user_details
        assert 'created_at' in user_details
        
        # Verify field values
        assert user_details['id'] == user.id
        assert user_details['email'] == 'provider2@example.com'
        assert user_details['first_name'] == 'John'
        assert user_details['last_name'] == 'Doe'
        assert user_details['role'] == 'PROVIDER'
        assert user_details['is_active'] is False

    def test_user_field_not_present_in_output(self, db):
        """
        Test that the 'user' field is not present in serialized output.
        Requirements: 1.1, 1.3
        """
        # Create user and provider profile
        user = User.objects.create_user(
            email='provider3@example.com',
            password='TestPass123!',
            first_name='Jane',
            last_name='Smith',
            role='PROVIDER',
            is_active=False
        )
        provider_profile = ProviderProfile.objects.create(
            user=user,
            service_description='Electrical services',
            approval_status='PENDING'
        )
        
        # Serialize the provider profile
        serializer = ProviderProfileSerializer(provider_profile)
        data = serializer.data
        
        # Assert 'user' field is NOT in the output
        assert 'user' not in data
        # But user_details should be present
        assert 'user_details' in data
