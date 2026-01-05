"""
Serializers for analytics data.
"""
from rest_framework import serializers
from apps.users.models import User, ProviderProfile
from apps.requests.models import ServiceRequest


class DashboardMetricsSerializer(serializers.Serializer):
    """Serializer for dashboard metrics."""
    total_users = serializers.IntegerField()
    total_regular_users = serializers.IntegerField()
    total_providers = serializers.IntegerField()
    active_providers = serializers.IntegerField()
    pending_applications = serializers.IntegerField()
    pending_requests = serializers.IntegerField()
    accepted_requests = serializers.IntegerField()
    completed_requests = serializers.IntegerField()
    rejected_requests = serializers.IntegerField()
    total_services = serializers.IntegerField()


class DateCountSerializer(serializers.Serializer):
    """Serializer for date-based count statistics."""
    date = serializers.DateField()
    count = serializers.IntegerField()


class ProviderActivitySerializer(serializers.Serializer):
    """Serializer for provider activity statistics."""
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    created_at = serializers.DateTimeField()
    services_count = serializers.IntegerField()
    received_requests_count = serializers.IntegerField()
    accepted_requests_count = serializers.IntegerField()
    completed_requests_count = serializers.IntegerField()


class UserSearchSerializer(serializers.ModelSerializer):
    """Serializer for user search results."""
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'is_active',
            'created_at'
        ]


class ProviderSearchSerializer(serializers.ModelSerializer):
    """Serializer for provider search results."""
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = ProviderProfile
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'service_description',
            'approval_status',
            'created_at',
            'approved_at'
        ]


class ServiceRequestSearchSerializer(serializers.ModelSerializer):
    """Serializer for service request search results."""
    service_name = serializers.CharField(source='service.name', read_only=True)
    requester_email = serializers.EmailField(source='requester.email', read_only=True)
    requester_name = serializers.CharField(source='requester.full_name', read_only=True)
    provider_email = serializers.EmailField(source='provider.email', read_only=True)
    provider_name = serializers.CharField(source='provider.full_name', read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id',
            'service_name',
            'requester_email',
            'requester_name',
            'provider_email',
            'provider_name',
            'status',
            'message',
            'created_at',
            'updated_at'
        ]
