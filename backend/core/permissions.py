from rest_framework import permissions


class IsRegularUser(permissions.BasePermission):
    """Permission class to check if user is a Regular User."""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'REGULAR'
        )


class IsServiceProvider(permissions.BasePermission):
    """Permission class to check if user is a Service Provider."""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'PROVIDER' and
            hasattr(request.user, 'provider_profile') and
            request.user.provider_profile.approval_status == 'APPROVED'
        )


class IsAdmin(permissions.BasePermission):
    """Permission class to check if user is an Admin."""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'ADMIN'
        )


class IsOwner(permissions.BasePermission):
    """Permission class to check if user is the owner of the object."""
    
    def has_object_permission(self, request, view, obj):
        # Check if the object has a user attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # Check if the object has a requester attribute
        if hasattr(obj, 'requester'):
            return obj.requester == request.user
        # Check if the object has a provider attribute
        if hasattr(obj, 'provider'):
            return obj.provider == request.user
        return False


class IsProviderOfService(permissions.BasePermission):
    """Permission class to check if user is the provider of a service."""
    
    def has_object_permission(self, request, view, obj):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(obj, 'provider') and
            obj.provider == request.user
        )


class IsRegularUserOrProvider(permissions.BasePermission):
    """Permission class to check if user is either a Regular User or Service Provider."""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['REGULAR', 'PROVIDER']
        )
