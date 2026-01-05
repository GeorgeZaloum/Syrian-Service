"""
Serializers for service request management API.
"""
from rest_framework import serializers
from .models import ServiceRequest
from apps.users.serializers import UserSerializer
from apps.services.serializers import ServiceSerializer


class ServiceRequestSerializer(serializers.ModelSerializer):
    """Serializer for ServiceRequest model."""
    
    requester = UserSerializer(read_only=True)
    provider = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    requester_name = serializers.CharField(source='requester.full_name', read_only=True)
    provider_name = serializers.CharField(source='provider.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id',
            'service',
            'service_name',
            'requester',
            'requester_name',
            'provider',
            'provider_name',
            'status',
            'message',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'service',
            'service_name',
            'requester',
            'requester_name',
            'provider',
            'provider_name',
            'status',
            'created_at',
            'updated_at'
        ]


class ServiceRequestCreateSerializer(serializers.Serializer):
    """Serializer for creating a service request."""
    
    service_id = serializers.IntegerField(required=True)
    message = serializers.CharField(required=False, allow_blank=True, style={'base_template': 'textarea.html'})
    
    def validate_service_id(self, value):
        """Validate that service_id is a positive integer."""
        if value <= 0:
            raise serializers.ValidationError("Service ID must be a positive integer.")
        return value
    
    def validate_message(self, value):
        """Validate message length if provided."""
        if value and len(value.strip()) > 1000:
            raise serializers.ValidationError("Message cannot exceed 1000 characters.")
        return value.strip() if value else ""


class ServiceRequestListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing service requests."""
    
    requester_name = serializers.CharField(source='requester.full_name', read_only=True)
    provider_name = serializers.CharField(source='provider.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_location = serializers.CharField(source='service.location', read_only=True)
    service_cost = serializers.DecimalField(source='service.cost', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id',
            'service_name',
            'service_location',
            'service_cost',
            'requester_name',
            'provider_name',
            'status',
            'message',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields
