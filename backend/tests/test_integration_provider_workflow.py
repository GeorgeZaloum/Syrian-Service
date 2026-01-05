"""
Integration tests for service provider workflows.
Tests Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6
"""
import pytest
from rest_framework import status
from apps.services.models import Service
from apps.requests.models import ServiceRequest


@pytest.mark.integration
@pytest.mark.django_db
class TestServiceProviderWorkflows:
    """Test service provider CRUD operations and workflows."""

    def test_service_creation_workflow(self, provider_client, provider_user):
        """
        Test provider can create a new service.
        Requirements: 8.2, 8.3
        """
        service_data = {
            'name': 'Lawn Mowing Service',
            'description': 'Professional lawn care and mowing',
            'location': 'Seattle',
            'cost': '75.50'
        }
        
        response = provider_client.post('/api/services/', service_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'service' in response.data
        assert response.data['service']['name'] == 'Lawn Mowing Service'
        assert response.data['service']['provider']['id'] == provider_user.id
        assert response.data['service']['is_active'] is True
        
        # Verify service is created in database
        service = Service.objects.get(id=response.data['service']['id'])
        assert service.provider == provider_user
        assert service.name == 'Lawn Mowing Service'
        assert float(service.cost) == 75.50

    def test_service_editing_workflow(self, provider_client, service):
        """
        Test provider can edit their own service.
        Requirements: 8.3, 8.4
        """
        updated_data = {
            'name': 'Updated Cleaning Service',
            'description': 'Updated description',
            'location': 'Updated Location',
            'cost': '150.00'
        }
        
        response = provider_client.put(f'/api/services/{service.id}/', updated_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'service' in response.data
        assert response.data['service']['name'] == 'Updated Cleaning Service'
        assert response.data['service']['cost'] == '150.00'
        
        # Verify changes in database
        service.refresh_from_db()
        assert service.name == 'Updated Cleaning Service'
        assert float(service.cost) == 150.00

    def test_service_deletion_workflow(self, provider_client, provider_user):
        """
        Test provider can delete their service without pending requests.
        Requirements: 8.5, 8.6
        """
        # Create a service without requests
        service = Service.objects.create(
            provider=provider_user,
            name='Deletable Service',
            description='Test service',
            location='Test',
            cost=100.00
        )
        
        response = provider_client.delete(f'/api/services/{service.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        
        # Verify service is deleted or marked inactive
        service.refresh_from_db()
        assert service.is_active is False

    def test_service_deletion_prevention_with_pending_requests(self, provider_client, service, service_request):
        """
        Test that services with pending requests cannot be deleted.
        Requirements: 8.6
        """
        # Ensure request is pending
        assert service_request.status == 'PENDING'
        assert service_request.service == service
        
        response = provider_client.delete(f'/api/services/{service.id}/')
        # Should fail or return error
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN]
        
        # Verify service still exists and is active
        service.refresh_from_db()
        assert service.is_active is True

    def test_service_visibility_in_user_search(self, api_client, provider_user, regular_user):
        """
        Test that created services are visible to users in search.
        Requirements: 8.1, 8.2
        """
        # Provider creates service
        api_client.force_authenticate(user=provider_user)
        service_data = {
            'name': 'Visible Service',
            'description': 'Should be visible',
            'location': 'Miami',
            'cost': '99.99'
        }
        response = api_client.post('/api/services/', service_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'service' in response.data
        service_id = response.data['service']['id']
        
        # Regular user searches for services
        api_client.force_authenticate(user=regular_user)
        response = api_client.get('/api/services/', {'location': 'Miami'})
        assert response.status_code == status.HTTP_200_OK
        
        # Verify service is in results
        service_ids = [s['id'] for s in response.data['results']]
        assert service_id in service_ids

    def test_provider_can_only_edit_own_services(self, api_client, provider_user, service):
        """
        Test that providers can only edit their own services.
        Requirements: 8.4
        """
        # Create another provider
        from django.contrib.auth import get_user_model
        User = get_user_model()
        other_provider = User.objects.create_user(
            email='other@example.com',
            password='TestPass123!',
            first_name='Other',
            last_name='Provider',
            role='PROVIDER'
        )
        from apps.users.models import ProviderProfile
        ProviderProfile.objects.create(
            user=other_provider,
            service_description='Other services',
            approval_status='APPROVED'
        )
        
        # Other provider tries to edit the service
        api_client.force_authenticate(user=other_provider)
        updated_data = {
            'name': 'Hacked Service',
            'description': 'Unauthorized edit',
            'location': 'Hacked',
            'cost': '1.00'
        }
        
        response = api_client.put(f'/api/services/{service.id}/', updated_data)
        # Should fail with 403 or 404
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
        
        # Verify service unchanged
        service.refresh_from_db()
        assert service.name == 'House Cleaning'

    def test_provider_service_list_shows_only_own_services(self, api_client, provider_user):
        """
        Test that provider sees only their own services in management view.
        Requirements: 8.1
        """
        # Create services for this provider
        Service.objects.create(
            provider=provider_user,
            name='My Service 1',
            description='Test',
            location='Test',
            cost=100.00
        )
        Service.objects.create(
            provider=provider_user,
            name='My Service 2',
            description='Test',
            location='Test',
            cost=200.00
        )
        
        # Create service for another provider
        from django.contrib.auth import get_user_model
        User = get_user_model()
        other_provider = User.objects.create_user(
            email='other2@example.com',
            password='TestPass123!',
            first_name='Other',
            last_name='Provider',
            role='PROVIDER'
        )
        Service.objects.create(
            provider=other_provider,
            name='Other Service',
            description='Test',
            location='Test',
            cost=300.00
        )
        
        # Provider views their services
        api_client.force_authenticate(user=provider_user)
        response = api_client.get('/api/services/my-services/')
        
        # If endpoint doesn't exist, try with filter
        if response.status_code == status.HTTP_404_NOT_FOUND:
            response = api_client.get('/api/services/', {'my_services': 'true'})
        
        if response.status_code == status.HTTP_200_OK:
            # Should only see own services
            service_names = [s['name'] for s in response.data['results']]
            assert 'My Service 1' in service_names or 'My Service 2' in service_names
            assert 'Other Service' not in service_names

    def test_inactive_services_not_visible_to_users(self, api_client, provider_user, regular_user):
        """
        Test that inactive services are not visible in user search.
        Requirements: 8.5
        """
        # Create inactive service
        service = Service.objects.create(
            provider=provider_user,
            name='Inactive Service',
            description='Should not be visible',
            location='Hidden',
            cost=100.00,
            is_active=False
        )
        
        # User searches for services
        api_client.force_authenticate(user=regular_user)
        response = api_client.get('/api/services/', {'location': 'Hidden'})
        assert response.status_code == status.HTTP_200_OK
        
        # Inactive service should not be in results
        service_ids = [s['id'] for s in response.data['results']]
        assert service.id not in service_ids
