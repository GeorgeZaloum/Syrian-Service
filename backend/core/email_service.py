"""
Email notification service for sending transactional emails.
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


class EmailNotificationService:
    """Service for sending email notifications."""
    
    @staticmethod
    def send_email(subject, recipient_email, template_name, context):
        """
        Send an email using a template.
        
        Args:
            subject: Email subject line
            recipient_email: Recipient's email address
            template_name: Name of the email template (without .html extension)
            context: Dictionary of context variables for the template
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Render HTML content from template
            html_message = render_to_string(f'emails/{template_name}.html', context)
            plain_message = strip_tags(html_message)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Email sent successfully to {recipient_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
            return False
    
    @classmethod
    def send_provider_approval_email(cls, provider_email, provider_name):
        """
        Send approval notification to service provider.
        
        Args:
            provider_email: Provider's email address
            provider_name: Provider's full name
            
        Returns:
            bool: True if email was sent successfully
        """
        subject = "Your Service Provider Application Has Been Approved"
        context = {
            'provider_name': provider_name,
            'login_url': f"{settings.FRONTEND_URL}/login" if hasattr(settings, 'FRONTEND_URL') else "http://localhost:5173/login",
        }
        
        return cls.send_email(
            subject=subject,
            recipient_email=provider_email,
            template_name='provider_approval',
            context=context
        )
    
    @classmethod
    def send_provider_rejection_email(cls, provider_email, provider_name):
        """
        Send rejection notification to service provider.
        
        Args:
            provider_email: Provider's email address
            provider_name: Provider's full name
            
        Returns:
            bool: True if email was sent successfully
        """
        subject = "Update on Your Service Provider Application"
        context = {
            'provider_name': provider_name,
            'support_email': settings.DEFAULT_FROM_EMAIL,
        }
        
        return cls.send_email(
            subject=subject,
            recipient_email=provider_email,
            template_name='provider_rejection',
            context=context
        )
    
    @classmethod
    def send_service_request_notification(cls, provider_email, provider_name, service_name, requester_name):
        """
        Send notification to provider when they receive a service request.
        
        Args:
            provider_email: Provider's email address
            provider_name: Provider's full name
            service_name: Name of the requested service
            requester_name: Name of the user requesting the service
            
        Returns:
            bool: True if email was sent successfully
        """
        subject = f"New Service Request for {service_name}"
        context = {
            'provider_name': provider_name,
            'service_name': service_name,
            'requester_name': requester_name,
            'dashboard_url': f"{settings.FRONTEND_URL}/provider/dashboard" if hasattr(settings, 'FRONTEND_URL') else "http://localhost:5173/provider/dashboard",
        }
        
        return cls.send_email(
            subject=subject,
            recipient_email=provider_email,
            template_name='service_request_notification',
            context=context
        )
    
    @classmethod
    def send_request_accepted_email(cls, requester_email, requester_name, service_name, provider_name):
        """
        Send notification to user when their service request is accepted.
        
        Args:
            requester_email: User's email address
            requester_name: User's full name
            service_name: Name of the requested service
            provider_name: Provider's full name
            
        Returns:
            bool: True if email was sent successfully
        """
        subject = f"Your Service Request for {service_name} Has Been Accepted"
        context = {
            'requester_name': requester_name,
            'service_name': service_name,
            'provider_name': provider_name,
            'dashboard_url': f"{settings.FRONTEND_URL}/user/dashboard" if hasattr(settings, 'FRONTEND_URL') else "http://localhost:5173/user/dashboard",
        }
        
        return cls.send_email(
            subject=subject,
            recipient_email=requester_email,
            template_name='request_accepted',
            context=context
        )
    
    @classmethod
    def send_request_rejected_email(cls, requester_email, requester_name, service_name, provider_name):
        """
        Send notification to user when their service request is rejected.
        
        Args:
            requester_email: User's email address
            requester_name: User's full name
            service_name: Name of the requested service
            provider_name: Provider's full name
            
        Returns:
            bool: True if email was sent successfully
        """
        subject = f"Update on Your Service Request for {service_name}"
        context = {
            'requester_name': requester_name,
            'service_name': service_name,
            'provider_name': provider_name,
            'search_url': f"{settings.FRONTEND_URL}/user/search" if hasattr(settings, 'FRONTEND_URL') else "http://localhost:5173/user/search",
        }
        
        return cls.send_email(
            subject=subject,
            recipient_email=requester_email,
            template_name='request_rejected',
            context=context
        )
