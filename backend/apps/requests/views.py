"""
Views for service request management API.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.exceptions import ValidationException, PermissionDeniedException, NotFoundException
from core.pagination import StandardResultsSetPagination
from .models import ServiceRequest
from .serializers import (
    ServiceRequestSerializer,
    ServiceRequestCreateSerializer,
    ServiceRequestListSerializer
)
from .services import ServiceRequestService


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def service_request_list_create(request):
    """
    List all service requests for the authenticated user (GET) or create a new service request (POST).
    
    GET /api/requests/
    Returns requests based on user role:
    - Regular users see requests they sent
    - Providers see requests they received
    - Admins see all requests
    
    POST /api/requests/
    Body: {
        "service_id": 1,
        "message": "Optional message"
    }
    """
    if request.method == 'GET':
        # List service requests based on user role
        requests_queryset = ServiceRequestService.get_user_requests(request.user)
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            valid_statuses = ['PENDING', 'ACCEPTED', 'REJECTED', 'COMPLETED']
            if status_filter.upper() in valid_statuses:
                requests_queryset = requests_queryset.filter(status=status_filter.upper())
        
        # Paginate results
        paginator = StandardResultsSetPagination()
        paginated_requests = paginator.paginate_queryset(requests_queryset, request)
        serializer = ServiceRequestListSerializer(paginated_requests, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        # Create service request - only for regular users
        if request.user.role != 'REGULAR':
            return Response(
                {
                    'error': {
                        'code': 'FORBIDDEN',
                        'message': 'Only regular users can create service requests.',
                        'details': {}
                    }
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        create_serializer = ServiceRequestCreateSerializer(data=request.data)
        
        if not create_serializer.is_valid():
            return Response(
                {
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Invalid input data',
                        'details': create_serializer.errors
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service_request = ServiceRequestService.create_service_request(
                requester=request.user,
                service_id=create_serializer.validated_data['service_id'],
                message=create_serializer.validated_data.get('message', '')
            )
            
            return Response(
                {
                    'message': 'Service request created successfully',
                    'request': ServiceRequestSerializer(service_request).data
                },
                status=status.HTTP_201_CREATED
            )
        
        except (ValidationException, NotFoundException) as e:
            error_code = 'VALIDATION_ERROR' if isinstance(e, ValidationException) else 'NOT_FOUND'
            http_status = status.HTTP_400_BAD_REQUEST if isinstance(e, ValidationException) else status.HTTP_404_NOT_FOUND
            
            return Response(
                {
                    'error': {
                        'code': error_code,
                        'message': str(e),
                        'details': e.details if hasattr(e, 'details') else {}
                    }
                },
                status=http_status
            )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def service_request_detail(request, request_id):
    """
    Retrieve a service request by ID.
    
    GET /api/requests/{id}/
    """
    try:
        service_request = ServiceRequestService.get_request_by_id(request_id)
    except NotFoundException as e:
        return Response(
            {
                'error': {
                    'code': 'NOT_FOUND',
                    'message': str(e),
                    'details': {}
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if user can access this request
    if not ServiceRequestService.can_user_access_request(request.user, service_request):
        return Response(
            {
                'error': {
                    'code': 'FORBIDDEN',
                    'message': 'You do not have permission to access this request.',
                    'details': {}
                }
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = ServiceRequestSerializer(service_request)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_service_request(request, request_id):
    """
    Accept a service request.
    
    POST /api/requests/{id}/accept/
    """
    # Check if user is a provider
    if request.user.role != 'PROVIDER':
        return Response(
            {
                'error': {
                    'code': 'FORBIDDEN',
                    'message': 'Only service providers can accept requests.',
                    'details': {}
                }
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        service_request = ServiceRequestService.get_request_by_id(request_id)
    except NotFoundException as e:
        return Response(
            {
                'error': {
                    'code': 'NOT_FOUND',
                    'message': str(e),
                    'details': {}
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        updated_request = ServiceRequestService.accept_service_request(
            service_request=service_request,
            provider=request.user
        )
        
        return Response(
            {
                'message': 'Service request accepted successfully',
                'request': ServiceRequestSerializer(updated_request).data
            },
            status=status.HTTP_200_OK
        )
    
    except (ValidationException, PermissionDeniedException) as e:
        error_code = 'VALIDATION_ERROR' if isinstance(e, ValidationException) else 'FORBIDDEN'
        http_status = status.HTTP_400_BAD_REQUEST if isinstance(e, ValidationException) else status.HTTP_403_FORBIDDEN
        
        return Response(
            {
                'error': {
                    'code': error_code,
                    'message': str(e),
                    'details': e.details if hasattr(e, 'details') else {}
                }
            },
            status=http_status
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_service_request(request, request_id):
    """
    Reject a service request.
    
    POST /api/requests/{id}/reject/
    """
    # Check if user is a provider
    if request.user.role != 'PROVIDER':
        return Response(
            {
                'error': {
                    'code': 'FORBIDDEN',
                    'message': 'Only service providers can reject requests.',
                    'details': {}
                }
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        service_request = ServiceRequestService.get_request_by_id(request_id)
    except NotFoundException as e:
        return Response(
            {
                'error': {
                    'code': 'NOT_FOUND',
                    'message': str(e),
                    'details': {}
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        updated_request = ServiceRequestService.reject_service_request(
            service_request=service_request,
            provider=request.user
        )
        
        return Response(
            {
                'message': 'Service request rejected successfully',
                'request': ServiceRequestSerializer(updated_request).data
            },
            status=status.HTTP_200_OK
        )
    
    except (ValidationException, PermissionDeniedException) as e:
        error_code = 'VALIDATION_ERROR' if isinstance(e, ValidationException) else 'FORBIDDEN'
        http_status = status.HTTP_400_BAD_REQUEST if isinstance(e, ValidationException) else status.HTTP_403_FORBIDDEN
        
        return Response(
            {
                'error': {
                    'code': error_code,
                    'message': str(e),
                    'details': e.details if hasattr(e, 'details') else {}
                }
            },
            status=http_status
        )
