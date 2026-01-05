"""
Service layer for service management business logic.
"""
from django.db import transaction
from core.exceptions import ValidationException, PermissionDeniedException, NotFoundException
from .models import Service
from .repositories import ServiceRepository


class ServiceManagementService:
    """Service for handling service CRUD operations."""
    
    @staticmethod
    @transaction.atomic
    def create_service(provider, name, description, location, cost):
        """
        Create a new service.
        
        Args:
            provider: User instance (must be a service provider)
            name: Service name
            description: Service description
            location: Service location
            cost: Service cost
            
        Returns:
            Service: The created service instance
            
        Raises:
            ValidationException: If validation fails
        """
        # Validate provider role
        if provider.role != 'PROVIDER':
            raise PermissionDeniedException("Only service providers can create services")
        
        # Validate provider is approved
        if not hasattr(provider, 'provider_profile') or provider.provider_profile.approval_status != 'APPROVED':
            raise PermissionDeniedException("Your provider account must be approved before creating services")
        
        # Validate required fields
        if not name or len(name.strip()) < 3:
            raise ValidationException(
                "Service name validation failed",
                details={'name': ['Service name must be at least 3 characters long.']}
            )
        
        if not description or len(description.strip()) < 10:
            raise ValidationException(
                "Service description validation failed",
                details={'description': ['Service description must be at least 10 characters long.']}
            )
        
        if not location or len(location.strip()) < 2:
            raise ValidationException(
                "Service location validation failed",
                details={'location': ['Service location must be at least 2 characters long.']}
            )
        
        if cost <= 0:
            raise ValidationException(
                "Service cost validation failed",
                details={'cost': ['Service cost must be greater than 0.']}
            )
        
        # Create service
        service = ServiceRepository.create(
            provider=provider,
            name=name.strip(),
            description=description.strip(),
            location=location.strip(),
            cost=cost
        )
        
        return service
    
    @staticmethod
    @transaction.atomic
    def update_service(service, provider, **kwargs):
        """
        Update an existing service.
        
        Args:
            service: Service instance to update
            provider: User instance (must be the service owner)
            **kwargs: Fields to update (name, description, location, cost)
            
        Returns:
            Service: The updated service instance
            
        Raises:
            PermissionDeniedException: If user is not the service owner
            ValidationException: If validation fails
        """
        # Verify ownership
        if service.provider != provider:
            raise PermissionDeniedException("You can only update your own services")
        
        # Validate fields if provided
        if 'name' in kwargs:
            name = kwargs['name']
            if not name or len(name.strip()) < 3:
                raise ValidationException(
                    "Service name validation failed",
                    details={'name': ['Service name must be at least 3 characters long.']}
                )
            kwargs['name'] = name.strip()
        
        if 'description' in kwargs:
            description = kwargs['description']
            if not description or len(description.strip()) < 10:
                raise ValidationException(
                    "Service description validation failed",
                    details={'description': ['Service description must be at least 10 characters long.']}
                )
            kwargs['description'] = description.strip()
        
        if 'location' in kwargs:
            location = kwargs['location']
            if not location or len(location.strip()) < 2:
                raise ValidationException(
                    "Service location validation failed",
                    details={'location': ['Service location must be at least 2 characters long.']}
                )
            kwargs['location'] = location.strip()
        
        if 'cost' in kwargs:
            cost = kwargs['cost']
            if cost <= 0:
                raise ValidationException(
                    "Service cost validation failed",
                    details={'cost': ['Service cost must be greater than 0.']}
                )
        
        # Update service
        updated_service = ServiceRepository.update(service, **kwargs)
        
        return updated_service
    
    @staticmethod
    @transaction.atomic
    def delete_service(service, provider):
        """
        Delete a service (soft delete).
        
        Args:
            service: Service instance to delete
            provider: User instance (must be the service owner)
            
        Returns:
            Service: The deleted service instance
            
        Raises:
            PermissionDeniedException: If user is not the service owner
            ValidationException: If service has pending requests
        """
        # Verify ownership
        if service.provider != provider:
            raise PermissionDeniedException("You can only delete your own services")
        
        # Check for pending requests
        if service.has_pending_requests():
            raise ValidationException(
                "Cannot delete service",
                details={'service': ['Cannot delete a service with pending requests. Please wait for all requests to be resolved.']}
            )
        
        # Soft delete
        deleted_service = ServiceRepository.delete(service)
        
        return deleted_service
    
    @staticmethod
    def get_service_by_id(service_id):
        """
        Get a service by ID.
        
        Args:
            service_id: Service ID
            
        Returns:
            Service: The service instance
            
        Raises:
            NotFoundException: If service not found
        """
        service = ServiceRepository.get_by_id(service_id)
        
        if not service or not service.is_active:
            raise NotFoundException("Service not found")
        
        return service
    
    @staticmethod
    def get_provider_services(provider):
        """
        Get all services for a provider.
        
        Args:
            provider: User instance
            
        Returns:
            QuerySet: Provider's services
        """
        return ServiceRepository.get_by_provider(provider)


class ServiceSearchService:
    """Service for handling service search and filtering."""
    
    @staticmethod
    def search_services(location=None, min_cost=None, max_cost=None):
        """
        Search services with optional filters.
        
        Args:
            location: Location filter (case-insensitive partial match)
            min_cost: Minimum cost filter
            max_cost: Maximum cost filter
            
        Returns:
            QuerySet: Filtered services
        """
        # Validate cost filters
        if min_cost is not None and min_cost < 0:
            raise ValidationException(
                "Invalid cost filter",
                details={'min_cost': ['Minimum cost cannot be negative.']}
            )
        
        if max_cost is not None and max_cost < 0:
            raise ValidationException(
                "Invalid cost filter",
                details={'max_cost': ['Maximum cost cannot be negative.']}
            )
        
        if min_cost is not None and max_cost is not None and min_cost > max_cost:
            raise ValidationException(
                "Invalid cost filter",
                details={'cost': ['Minimum cost cannot be greater than maximum cost.']}
            )
        
        # Search services
        services = ServiceRepository.search(
            location=location,
            min_cost=min_cost,
            max_cost=max_cost
        )
        
        return services
