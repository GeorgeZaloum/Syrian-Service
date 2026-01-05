"""
Serializers for user management API.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, ProviderProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'role', 'is_active', 'created_at']
        read_only_fields = ['id', 'role', 'is_active', 'created_at']


class ProviderProfileSerializer(serializers.ModelSerializer):
    """Serializer for ProviderProfile model."""
    
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = ProviderProfile
        fields = ['id', 'user_details', 'service_description', 'approval_status', 'approved_by', 'approved_at', 'created_at']
        read_only_fields = ['id', 'approval_status', 'approved_by', 'approved_at', 'created_at']


class RegularUserRegistrationSerializer(serializers.Serializer):
    """Serializer for regular user registration."""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True, max_length=100)
    last_name = serializers.CharField(required=True, max_length=100)
    role = serializers.CharField(required=False, write_only=True)  # Accept but ignore role field
    service_description = serializers.CharField(required=False, write_only=True, allow_blank=True)  # Accept but ignore for regular users
    
    def validate_email(self, value):
        """Validate email uniqueness."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_password(self, value):
        """Validate password strength."""
        validate_password(value)
        return value


class ServiceProviderRegistrationSerializer(serializers.Serializer):
    """Serializer for service provider registration."""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True, max_length=100)
    last_name = serializers.CharField(required=True, max_length=100)
    service_description = serializers.CharField(required=True, style={'base_template': 'textarea.html'})
    role = serializers.CharField(required=False, write_only=True)  # Accept but ignore role field
    
    def validate_email(self, value):
        """Validate email uniqueness."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_password(self, value):
        """Validate password strength."""
        validate_password(value)
        return value
    
    def validate_service_description(self, value):
        """Validate service description length."""
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Service description must be at least 10 characters long.")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""
    
    current_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    def validate_new_password(self, value):
        """Validate new password strength."""
        validate_password(value, user=self.context.get('request').user)
        return value
