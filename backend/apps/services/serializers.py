"""
Serializers for service management API.
"""
from rest_framework import serializers
from .models import Service
from apps.users.serializers import UserSerializer


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service model."""
    
    provider = UserSerializer(read_only=True)
    provider_name = serializers.CharField(source='provider.full_name', read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id',
            'provider',
            'provider_name',
            'name',
            'description',
            'location',
            'cost',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'provider', 'provider_name', 'is_active', 'created_at', 'updated_at']


class ServiceCreateSerializer(serializers.Serializer):
    """Serializer for creating a service."""
    
    name = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(required=True, style={'base_template': 'textarea.html'})
    location = serializers.CharField(required=True, max_length=200)
    cost = serializers.DecimalField(required=True, max_digits=10, decimal_places=2, min_value=0.01)
    
    def validate_name(self, value):
        """Validate service name length."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Service name must be at least 3 characters long.")
        return value
    
    def validate_description(self, value):
        """Validate service description length."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Service description must be at least 10 characters long.")
        return value
    
    def validate_location(self, value):
        """Validate service location length."""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Service location must be at least 2 characters long.")
        return value


class ServiceUpdateSerializer(serializers.Serializer):
    """Serializer for updating a service."""
    
    name = serializers.CharField(required=False, max_length=200)
    description = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    location = serializers.CharField(required=False, max_length=200)
    cost = serializers.DecimalField(required=False, max_digits=10, decimal_places=2, min_value=0.01)
    
    def validate_name(self, value):
        """Validate service name length."""
        if value and len(value.strip()) < 3:
            raise serializers.ValidationError("Service name must be at least 3 characters long.")
        return value
    
    def validate_description(self, value):
        """Validate service description length."""
        if value and len(value.strip()) < 10:
            raise serializers.ValidationError("Service description must be at least 10 characters long.")
        return value
    
    def validate_location(self, value):
        """Validate service location length."""
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError("Service location must be at least 2 characters long.")
        return value


class ServiceSearchSerializer(serializers.Serializer):
    """Serializer for service search parameters."""
    
    location = serializers.CharField(required=False, allow_blank=True)
    min_cost = serializers.DecimalField(required=False, max_digits=10, decimal_places=2, min_value=0)
    max_cost = serializers.DecimalField(required=False, max_digits=10, decimal_places=2, min_value=0)
    
    def validate(self, data):
        """Validate that min_cost is not greater than max_cost."""
        min_cost = data.get('min_cost')
        max_cost = data.get('max_cost')
        
        if min_cost is not None and max_cost is not None and min_cost > max_cost:
            raise serializers.ValidationError({
                'cost': 'Minimum cost cannot be greater than maximum cost.'
            })
        
        return data
