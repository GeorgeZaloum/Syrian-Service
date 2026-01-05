from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404


class ServiceMarketplaceException(Exception):
    """Base exception for Service Marketplace Platform."""
    
    def __init__(self, message, code=None):
        self.message = message
        self.code = code or 'SERVICE_MARKETPLACE_ERROR'
        super().__init__(self.message)


class UnauthorizedException(ServiceMarketplaceException):
    """Exception raised when user is not authorized."""
    
    def __init__(self, message="User not authorized"):
        super().__init__(message, code='UNAUTHORIZED')


class ValidationException(ServiceMarketplaceException):
    """Exception raised when data validation fails."""
    
    def __init__(self, message="Data validation failed", details=None):
        super().__init__(message, code='VALIDATION_ERROR')
        self.details = details


class NotFoundException(ServiceMarketplaceException):
    """Exception raised when resource is not found."""
    
    def __init__(self, message="Resource not found"):
        super().__init__(message, code='NOT_FOUND')


class PermissionDeniedException(ServiceMarketplaceException):
    """Exception raised when user doesn't have permission."""
    
    def __init__(self, message="Permission denied"):
        super().__init__(message, code='PERMISSION_DENIED')


class BusinessLogicException(ServiceMarketplaceException):
    """Exception raised when business logic validation fails."""
    
    def __init__(self, message="Business logic validation failed"):
        super().__init__(message, code='BUSINESS_LOGIC_ERROR')


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that returns consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Handle custom exceptions
    if isinstance(exc, ServiceMarketplaceException):
        error_response = {
            'error': {
                'code': exc.code,
                'message': exc.message,
            }
        }
        
        # Add details if available (for ValidationException)
        if hasattr(exc, 'details') and exc.details:
            error_response['error']['details'] = exc.details
        
        # Determine status code based on exception type
        if isinstance(exc, UnauthorizedException):
            status_code = status.HTTP_401_UNAUTHORIZED
        elif isinstance(exc, PermissionDeniedException):
            status_code = status.HTTP_403_FORBIDDEN
        elif isinstance(exc, NotFoundException):
            status_code = status.HTTP_404_NOT_FOUND
        elif isinstance(exc, ValidationException):
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            status_code = status.HTTP_400_BAD_REQUEST
        
        return Response(error_response, status=status_code)
    
    # Handle Django validation errors
    if isinstance(exc, DjangoValidationError):
        error_response = {
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Data validation failed',
                'details': exc.message_dict if hasattr(exc, 'message_dict') else str(exc)
            }
        }
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle 404 errors
    if isinstance(exc, Http404):
        error_response = {
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Resource not found'
            }
        }
        return Response(error_response, status=status.HTTP_404_NOT_FOUND)
    
    # If response is None, return a generic error response
    if response is None:
        error_response = {
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'An unexpected error occurred'
            }
        }
        return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Format DRF validation errors
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        error_response = {
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Invalid input data',
                'details': response.data
            }
        }
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    
    # Format other DRF errors
    if hasattr(response, 'data'):
        error_response = {
            'error': {
                'code': 'ERROR',
                'message': response.data.get('detail', 'An error occurred') if isinstance(response.data, dict) else str(response.data)
            }
        }
        return Response(error_response, status=response.status_code)
    
    return response
