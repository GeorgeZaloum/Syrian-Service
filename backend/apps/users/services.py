"""
Service layer for user management business logic.
"""
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from core.exceptions import ValidationException, BusinessLogicException
from core.email_service import EmailNotificationService
from .models import User, ProviderProfile


class UserRegistrationService:
    """Service for handling user registration logic."""
    
    @staticmethod
    @transaction.atomic
    def register_regular_user(email, password, first_name, last_name):
        """
        Register a new regular user.
        
        Args:
            email: User's email address
            password: User's password
            first_name: User's first name
            last_name: User's last name
            
        Returns:
            User: The created user instance
            
        Raises:
            ValidationException: If validation fails
        """
        # Validate email uniqueness
        if User.objects.filter(email=email).exists():
            raise ValidationException(
                "Registration failed",
                details={'email': ['A user with this email already exists.']}
            )
        
        # Validate password strength
        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise ValidationException(
                "Password validation failed",
                details={'password': list(e.messages)}
            )
        
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='REGULAR',
            is_active=True
        )
        
        return user
    
    @staticmethod
    @transaction.atomic
    def register_service_provider(email, password, first_name, last_name, service_description):
        """
        Register a new service provider with pending approval status.
        
        Args:
            email: Provider's email address
            password: Provider's password
            first_name: Provider's first name
            last_name: Provider's last name
            service_description: Description of services offered
            
        Returns:
            tuple: (User instance, ProviderProfile instance)
            
        Raises:
            ValidationException: If validation fails
        """
        # Validate email uniqueness
        if User.objects.filter(email=email).exists():
            raise ValidationException(
                "Registration failed",
                details={'email': ['A user with this email already exists.']}
            )
        
        # Validate password strength
        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise ValidationException(
                "Password validation failed",
                details={'password': list(e.messages)}
            )
        
        # Validate service description
        if not service_description or len(service_description.strip()) < 10:
            raise ValidationException(
                "Service description validation failed",
                details={'service_description': ['Service description must be at least 10 characters long.']}
            )
        
        # Create user with inactive status (pending approval)
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='PROVIDER',
            is_active=False  # Inactive until approved
        )
        
        # Create provider profile
        provider_profile = ProviderProfile.objects.create(
            user=user,
            service_description=service_description,
            approval_status='PENDING'
        )
        
        return user, provider_profile


class PasswordChangeService:
    """Service for handling password change logic."""
    
    @staticmethod
    def change_password(user, current_password, new_password):
        """
        Change user's password after verifying current password.
        
        Args:
            user: User instance
            current_password: Current password for verification
            new_password: New password to set
            
        Returns:
            bool: True if password was changed successfully
            
        Raises:
            ValidationException: If validation fails
        """
        # Verify current password
        if not user.check_password(current_password):
            raise ValidationException(
                "Password change failed",
                details={'current_password': ['Current password is incorrect.']}
            )
        
        # Validate new password strength
        try:
            validate_password(new_password, user=user)
        except DjangoValidationError as e:
            raise ValidationException(
                "New password validation failed",
                details={'new_password': list(e.messages)}
            )
        
        # Check if new password is different from current
        if user.check_password(new_password):
            raise ValidationException(
                "Password change failed",
                details={'new_password': ['New password must be different from current password.']}
            )
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return True



class ProviderApprovalService:
    """Service for handling provider approval workflow."""
    
    @staticmethod
    @transaction.atomic
    def approve_provider(provider_profile, admin_user):
        """
        Approve a provider application and send approval email.
        
        Args:
            provider_profile: ProviderProfile instance to approve
            admin_user: Admin user performing the approval
            
        Returns:
            ProviderProfile: The approved provider profile
            
        Raises:
            ValidationException: If validation fails
        """
        if provider_profile.approval_status == 'APPROVED':
            raise ValidationException(
                "Provider already approved",
                details={'approval_status': ['This provider has already been approved.']}
            )
        
        # Approve the provider
        provider_profile.approve(admin_user)
        
        # Send approval email
        EmailNotificationService.send_provider_approval_email(
            provider_email=provider_profile.user.email,
            provider_name=provider_profile.user.full_name
        )
        
        return provider_profile
    
    @staticmethod
    @transaction.atomic
    def reject_provider(provider_profile, admin_user):
        """
        Reject a provider application and send rejection email.
        
        Args:
            provider_profile: ProviderProfile instance to reject
            admin_user: Admin user performing the rejection
            
        Returns:
            ProviderProfile: The rejected provider profile
            
        Raises:
            ValidationException: If validation fails
        """
        if provider_profile.approval_status == 'REJECTED':
            raise ValidationException(
                "Provider already rejected",
                details={'approval_status': ['This provider has already been rejected.']}
            )
        
        # Reject the provider
        provider_profile.reject(admin_user)
        
        # Send rejection email
        EmailNotificationService.send_provider_rejection_email(
            provider_email=provider_profile.user.email,
            provider_name=provider_profile.user.full_name
        )
        
        return provider_profile
    
    @staticmethod
    def get_pending_applications():
        """
        Get all pending provider applications.
        
        Returns:
            QuerySet: Pending provider profiles
        """
        return ProviderProfile.objects.filter(
            approval_status='PENDING'
        ).select_related('user').order_by('-created_at')
