"""
Pytest configuration and shared fixtures for integration tests.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.services.models import Service
from apps.requests.models import ServiceRequest
from apps.problems.models import ProblemReport

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an API client for making requests."""
    return APIClient()


@pytest.fixture
def regular_user(db):
    """Create and return a regular user."""
    return User.objects.create_user(
        email='user@example.com',
        password='TestPass123!',
        first_name='John',
        last_name='Doe',
        role='REGULAR'
    )


@pytest.fixture
def provider_user(db):
    """Create and return an approved service provider."""
    user = User.objects.create_user(
        email='provider@example.com',
        password='TestPass123!',
        first_name='Jane',
        last_name='Smith',
        role='PROVIDER'
    )
    # Create provider profile
    from apps.users.models import ProviderProfile
    ProviderProfile.objects.create(
        user=user,
        service_description='Professional cleaning services',
        approval_status='APPROVED'
    )
    return user


@pytest.fixture
def pending_provider_user(db):
    """Create and return a pending service provider."""
    user = User.objects.create_user(
        email='pending@example.com',
        password='TestPass123!',
        first_name='Bob',
        last_name='Johnson',
        role='PROVIDER'
    )
    # Create provider profile with pending status
    from apps.users.models import ProviderProfile
    ProviderProfile.objects.create(
        user=user,
        service_description='Plumbing services',
        approval_status='PENDING'
    )
    return user


@pytest.fixture
def admin_user(db):
    """Create and return an admin user."""
    return User.objects.create_user(
        email='admin@example.com',
        password='TestPass123!',
        first_name='Admin',
        last_name='User',
        role='ADMIN',
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def service(db, provider_user):
    """Create and return a service."""
    return Service.objects.create(
        provider=provider_user,
        name='House Cleaning',
        description='Professional house cleaning service',
        location='New York',
        cost=100.00,
        is_active=True
    )


@pytest.fixture
def service_request(db, service, regular_user):
    """Create and return a service request."""
    return ServiceRequest.objects.create(
        service=service,
        requester=regular_user,
        provider=service.provider,
        message='I need cleaning service for my apartment',
        status='PENDING'
    )


@pytest.fixture
def authenticated_client(api_client, regular_user):
    """Return an authenticated API client for regular user."""
    api_client.force_authenticate(user=regular_user)
    return api_client


@pytest.fixture
def provider_client(api_client, provider_user):
    """Return an authenticated API client for provider."""
    api_client.force_authenticate(user=provider_user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Return an authenticated API client for admin."""
    api_client.force_authenticate(user=admin_user)
    return api_client
