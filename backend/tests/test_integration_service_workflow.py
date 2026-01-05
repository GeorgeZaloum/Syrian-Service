"""
Integration tests for service discovery and request workflow.
Tests Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4, 7.1, 7.2, 7.3, 7.4, 7.5
"""
import pytest
from rest_framework import status
from apps.services.models import Service
from apps.requests.models import ServiceRequest


@pytest.mark.integration
@pytest.mark.django_db
class TestServiceDiscoveryAndRequestWorkflow:
    """Test complete service discovery and request workflows."""

    def test_service_search_with_filters(self, authenticated_client, provider_user):
        """
        Test service search with location and cost filters.
        Requirements: 3.1, 3.2, 3.3, 3.4, 3.5
        """
        # Create multiple services with different locations and costs
        Service.objects.create(
            provider=provider_user,
            name='Cleaning Service NYC',
            description='NYC cleaning',
            location='New York',
            cost=100.00,
            is_active=True
        )
        Service.objects.create(
            provider=provider_user,
            name='Cleaning Service LA',
            description='LA cleaning',
            location='Los Angeles',
            cost=150.00,
            is_active=True
        )
        Service.objects.create(
            provider=provider_user,
            name='Budget Cleaning NYC',
            description='Affordable cleaning',
            location='New York',
            cost=50.00,
            is_active=True
        )
        
        # Test 1: Search all services
        response = authenticated_client.get('/api/services/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
        
        # Test 2: Filter by location
        response = authenticated_client.get('/api/services/', {'location': 'New York'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        for service in response.data['results']:
            assert service['location'] == 'New York'
        
        # Test 3: Filter by cost range
        response = authenticated_client.get('/api/services/', {
            'min_cost': '75',
            'max_cost': '125'
        })
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['cost'] == '100.00'
        
        # Test 4: Combined filters
        response = authenticated_client.get('/api/services/', {
            'location': 'New York',
            'max_cost': '75'
        })
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == 'Budget Cleaning NYC'

    def test_complete_service_request_workflow(self, api_client, regular_user, provider_user):
        """
        Test complete workflow: search, request, provider response, notifications.
        Requirements: 4.1, 4.2, 4.3, 4.4, 7.1, 7.2, 7.3, 7.4, 7.5
        """
        # Step 1: Provider creates a service
        api_client.force_authenticate(user=provider_user)
        service_data = {
            'name': 'Premium Cleaning',
            'description': 'High-quality cleaning service',
            'location': 'Boston',
            'cost': '200.00'
        }
        response = api_client.post('/api/services/', service_data)
        assert response.status_code == status.HTTP_201_CREATED
        service_id = response.data['id']
        
        # Step 2: Regular user searches and finds the service
        api_client.force_authenticate(user=regular_user)
        response = api_client.get('/api/services/', {'location': 'Boston'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['id'] == service_id
        
        # Step 3: User submits service request
        request_data = {
            'service': service_id,
            'message': 'I need cleaning for my office'
        }
        response = api_client.post('/api/requests/', request_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'PENDING'
        request_id = response.data['id']
        
        # Verify request is created
        service_request = ServiceRequest.objects.get(id=request_id)
        assert service_request.requester == regular_user
        assert service_request.provider == provider_user
        assert service_request.status == 'PENDING'
        
        # Step 4: User views their sent requests
        response = api_client.get('/api/requests/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
        user_request = next(r for r in response.data['results'] if r['id'] == request_id)
        assert user_request['status'] == 'PENDING'
        
        # Step 5: Provider views received requests
        api_client.force_authenticate(user=provider_user)
        response = api_client.get('/api/requests/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
        provider_request = next(r for r in response.data['results'] if r['id'] == request_id)
        assert provider_request['status'] == 'PENDING'
        
        # Step 6: Provider accepts the request
        response = api_client.post(f'/api/requests/{request_id}/accept/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'ACCEPTED'
        
        # Verify status updated
        service_request.refresh_from_db()
        assert service_request.status == 'ACCEPTED'
        
        # Step 7: User sees updated status
        api_client.force_authenticate(user=regular_user)
        response = api_client.get(f'/api/requests/{request_id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'ACCEPTED'

    def test_provider_reject_request_workflow(self, api_client, regular_user, provider_user, service):
        """
        Test provider rejecting a service request.
        Requirements: 7.2, 7.3, 7.4
        """
        # User creates request
        api_client.force_authenticate(user=regular_user)
        request_data = {
            'service': service.id,
            'message': 'Need service'
        }
        response = api_client.post('/api/requests/', request_data)
        assert response.status_code == status.HTTP_201_CREATED
        request_id = response.data['id']
        
        # Provider rejects request
        api_client.force_authenticate(user=provider_user)
        response = api_client.post(f'/api/requests/{request_id}/reject/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'REJECTED'
        
        # Verify status
        service_request = ServiceRequest.objects.get(id=request_id)
        assert service_request.status == 'REJECTED'

    def test_request_status_filtering(self, api_client, regular_user, provider_user, service):
        """
        Test filtering requests by status.
        Requirements: 4.3, 7.5
        """
        # Create multiple requests with different statuses
        api_client.force_authenticate(user=regular_user)
        
        # Create pending request
        response = api_client.post('/api/requests/', {
            'service': service.id,
            'message': 'Request 1'
        })
        pending_id = response.data['id']
        
        # Create and accept another request
        response = api_client.post('/api/requests/', {
            'service': service.id,
            'message': 'Request 2'
        })
        accepted_id = response.data['id']
        
        api_client.force_authenticate(user=provider_user)
        api_client.post(f'/api/requests/{accepted_id}/accept/')
        
        # Filter by status
        api_client.force_authenticate(user=regular_user)
        response = api_client.get('/api/requests/', {'status': 'PENDING'})
        assert response.status_code == status.HTTP_200_OK
        pending_requests = [r for r in response.data['results'] if r['status'] == 'PENDING']
        assert len(pending_requests) >= 1
        
        response = api_client.get('/api/requests/', {'status': 'ACCEPTED'})
        assert response.status_code == status.HTTP_200_OK
        accepted_requests = [r for r in response.data['results'] if r['status'] == 'ACCEPTED']
        assert len(accepted_requests) >= 1

    def test_role_based_request_filtering(self, api_client, regular_user, provider_user, service):
        """
        Test that users see sent requests and providers see received requests.
        Requirements: 7.1, 7.5
        """
        # User creates request
        api_client.force_authenticate(user=regular_user)
        response = api_client.post('/api/requests/', {
            'service': service.id,
            'message': 'Test request'
        })
        request_id = response.data['id']
        
        # User should see it in their sent requests
        response = api_client.get('/api/requests/')
        assert response.status_code == status.HTTP_200_OK
        user_requests = response.data['results']
        assert any(r['id'] == request_id for r in user_requests)
        
        # Provider should see it in their received requests
        api_client.force_authenticate(user=provider_user)
        response = api_client.get('/api/requests/')
        assert response.status_code == status.HTTP_200_OK
        provider_requests = response.data['results']
        assert any(r['id'] == request_id for r in provider_requests)

    def test_unauthorized_request_actions(self, api_client, regular_user, provider_user, service_request):
        """
        Test that only the provider can accept/reject requests.
        Requirements: 7.2
        """
        # Regular user tries to accept request (should fail)
        api_client.force_authenticate(user=regular_user)
        response = api_client.post(f'/api/requests/{service_request.id}/accept/')
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
        
        # Verify status unchanged
        service_request.refresh_from_db()
        assert service_request.status == 'PENDING'
