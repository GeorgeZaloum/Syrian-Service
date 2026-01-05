from django.db.models import Q
from .models import Service


class ServiceRepository:
    """Repository for Service data access operations."""
    
    @staticmethod
    def get_all_active():
        """Get all active services."""
        return Service.objects.filter(is_active=True).select_related('provider')
    
    @staticmethod
    def get_by_id(service_id):
        """Get service by ID."""
        try:
            return Service.objects.select_related('provider').get(id=service_id)
        except Service.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_provider(provider):
        """Get all services by a specific provider."""
        return Service.objects.filter(provider=provider).order_by('-created_at')
    
    @staticmethod
    def create(provider, name, description, location, cost):
        """Create a new service."""
        service = Service.objects.create(
            provider=provider,
            name=name,
            description=description,
            location=location,
            cost=cost
        )
        return service
    
    @staticmethod
    def update(service, **kwargs):
        """Update service fields."""
        for field, value in kwargs.items():
            if hasattr(service, field):
                setattr(service, field, value)
        service.save()
        return service
    
    @staticmethod
    def delete(service):
        """Delete a service (soft delete by setting is_active to False)."""
        service.is_active = False
        service.save()
        return service
    
    @staticmethod
    def hard_delete(service):
        """Permanently delete a service."""
        service.delete()
    
    @staticmethod
    def search(location=None, min_cost=None, max_cost=None):
        """Search services with filters."""
        queryset = Service.objects.filter(is_active=True).select_related('provider')
        
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        if min_cost is not None:
            queryset = queryset.filter(cost__gte=min_cost)
        
        if max_cost is not None:
            queryset = queryset.filter(cost__lte=max_cost)
        
        return queryset.order_by('cost', 'name')
    
    @staticmethod
    def count_by_provider(provider):
        """Count services by provider."""
        return Service.objects.filter(provider=provider, is_active=True).count()
