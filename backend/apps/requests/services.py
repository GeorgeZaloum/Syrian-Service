"""
Service layer for service request management business logic.
"""
from django.db import transaction
from django.db.models import Q
from core.email_service import EmailNotificationService
from core.exceptions import ValidationException, NotFoundException, PermissionDeniedException
from .models import ServiceRequest
from apps.services.models import Service


class ServiceRequestService:
    """Service for managing service request business logic."""
    
    @staticmethod
    def create_service_request(requester, service_id, message=""):
        """
        Create a new service request.
        
        Args:
            requester: User instance (requester)
            service_id: ID of the service being requested
            message: Optional message from requester
            
        Returns:
            ServiceRequest instance
            
        Raises:
            ValidationException: If validation fails
            NotFoundException: If service not found
        """
        # Validate requester role
        if requester.role != 'REGULAR':
            raise ValidationException(
                "Only regular users can create service requests.",
                details={'role': 'Invalid user role'}
            )
        
        # Get service
        try:
            service = Service.objects.select_related('provider').get(id=service_id, is_active=True)
        except Service.DoesNotExist:
            raise NotFoundException(f"Service with ID {service_id} not found or is inactive.")
        
        # Validate provider is approved
        if service.provider.role != 'PROVIDER':
            raise ValidationException(
                "Service provider is not valid.",
                details={'provider': 'Invalid provider'}
            )
        
        # Check if provider has an approved profile
        if not hasattr(service.provider, 'provider_profile') or service.provider.provider_profile.approval_status != 'APPROVED':
            raise ValidationException(
                "Service provider is not approved.",
                details={'provider': 'Provider not approved'}
            )
        
        # Create service request
        with transaction.atomic():
            service_request = ServiceRequest.objects.create(
                service=service,
                requester=requester,
                provider=service.provider,
                message=message,
                status='PENDING'
            )
            
            # Send notification to provider
            ServiceRequestNotificationService.notify_provider_new_request(service_request)
        
        return service_request
    
    @staticmethod
    def get_user_requests(user):
        """
        Get all service requests for a user based on their role.
        
        Args:
            user: User instance
            
        Returns:
            QuerySet of ServiceRequest instances
        """
        if user.role == 'REGULAR':
            # Regular users see requests they sent
            return ServiceRequest.objects.filter(
                requester=user
            ).select_related('service', 'provider', 'requester').order_by('-created_at')
        
        elif user.role == 'PROVIDER':
            # Providers see requests they received
            return ServiceRequest.objects.filter(
                provider=user
            ).select_related('service', 'provider', 'requester').order_by('-created_at')
        
        elif user.role == 'ADMIN':
            # Admins see all requests
            return ServiceRequest.objects.all().select_related(
                'service', 'provider', 'requester'
            ).order_by('-created_at')
        
        return ServiceRequest.objects.none()
    
    @staticmethod
    def get_request_by_id(request_id):
        """
        Get a service request by ID.
        
        Args:
            request_id: ID of the service request
            
        Returns:
            ServiceRequest instance
            
        Raises:
            NotFoundException: If request not found
        """
        try:
            return ServiceRequest.objects.select_related(
                'service', 'provider', 'requester'
            ).get(id=request_id)
        except ServiceRequest.DoesNotExist:
            raise NotFoundException(f"Service request with ID {request_id} not found.")
    
    @staticmethod
    def can_user_access_request(user, service_request):
        """
        Check if user can access a service request.
        
        Args:
            user: User instance
            service_request: ServiceRequest instance
            
        Returns:
            bool: True if user can access the request
        """
        if user.role == 'ADMIN':
            return True
        
        return service_request.requester == user or service_request.provider == user
    
    @staticmethod
    def accept_service_request(service_request, provider):
        """
        Accept a service request.
        
        Args:
            service_request: ServiceRequest instance
            provider: User instance (provider)
            
        Returns:
            ServiceRequest instance
            
        Raises:
            PermissionDeniedException: If user is not the provider
            ValidationException: If request cannot be accepted
        """
        # Validate provider
        if service_request.provider != provider:
            raise PermissionDeniedException("Only the service provider can accept this request.")
        
        # Validate current status
        if service_request.status != 'PENDING':
            raise ValidationException(
                f"Cannot accept request with status '{service_request.status}'. Only pending requests can be accepted.",
                details={'status': 'Invalid status'}
            )
        
        # Update status
        with transaction.atomic():
            service_request.status = 'ACCEPTED'
            service_request.save()
            
            # Send notification to requester
            ServiceRequestNotificationService.notify_requester_request_accepted(service_request)
        
        return service_request
    
    @staticmethod
    def reject_service_request(service_request, provider):
        """
        Reject a service request.
        
        Args:
            service_request: ServiceRequest instance
            provider: User instance (provider)
            
        Returns:
            ServiceRequest instance
            
        Raises:
            PermissionDeniedException: If user is not the provider
            ValidationException: If request cannot be rejected
        """
        # Validate provider
        if service_request.provider != provider:
            raise PermissionDeniedException("Only the service provider can reject this request.")
        
        # Validate current status
        if service_request.status != 'PENDING':
            raise ValidationException(
                f"Cannot reject request with status '{service_request.status}'. Only pending requests can be rejected.",
                details={'status': 'Invalid status'}
            )
        
        # Update status
        with transaction.atomic():
            service_request.status = 'REJECTED'
            service_request.save()
            
            # Send notification to requester
            ServiceRequestNotificationService.notify_requester_request_rejected(service_request)
        
        return service_request


class ServiceRequestNotificationService:
    """Service for handling service request email notifications."""
    
    @staticmethod
    def notify_provider_new_request(service_request):
        """
        Send email notification to provider when they receive a new service request.
        
        Args:
            service_request: ServiceRequest instance
            
        Returns:
            bool: True if email was sent successfully
        """
        return EmailNotificationService.send_service_request_notification(
            provider_email=service_request.provider.email,
            provider_name=service_request.provider.full_name,
            service_name=service_request.service.name,
            requester_name=service_request.requester.full_name
        )
    
    @staticmethod
    def notify_requester_request_accepted(service_request):
        """
        Send email notification to requester when their request is accepted.
        
        Args:
            service_request: ServiceRequest instance
            
        Returns:
            bool: True if email was sent successfully
        """
        return EmailNotificationService.send_request_accepted_email(
            requester_email=service_request.requester.email,
            requester_name=service_request.requester.full_name,
            service_name=service_request.service.name,
            provider_name=service_request.provider.full_name
        )
    
    @staticmethod
    def notify_requester_request_rejected(service_request):
        """
        Send email notification to requester when their request is rejected.
        
        Args:
            service_request: ServiceRequest instance
            
        Returns:
            bool: True if email was sent successfully
        """
        return EmailNotificationService.send_request_rejected_email(
            requester_email=service_request.requester.email,
            requester_name=service_request.requester.full_name,
            service_name=service_request.service.name,
            provider_name=service_request.provider.full_name
        )


# Note: The ServiceRequestService class will be implemented in task 5.2
# and will use the ServiceRequestNotificationService methods above to send
# email notifications when service requests are created, accepted, or rejected.
