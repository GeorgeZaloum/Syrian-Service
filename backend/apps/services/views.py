"""
Views for service management API.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.exceptions import ValidationException, PermissionDeniedException, NotFoundException
from core.permissions import IsServiceProvider
from core.pagination import StandardResultsSetPagination
from .models import Service
from .serializers import (
    ServiceSerializer,
    ServiceCreateSerializer,
    ServiceUpdateSerializer,
    ServiceSearchSerializer
)
from .services import ServiceManagementService, ServiceSearchService


@api_view(['GET', 'POST'])
def service_list_create(request):
    """
    List all services with optional filters (GET) or create a new service (POST).
    
    GET /api/services/
    Query params: location, min_cost, max_cost
    
    POST /api/services/
    Body: {
        "name": "Service Name",
        "description": "Service Description",
        "location": "Location",
        "cost": 100.00
    }
    """
    if request.method == 'GET':
        # Search/list services - available to all users (authenticated or not)
        search_serializer = ServiceSearchSerializer(data=request.query_params)
        
        if not search_serializer.is_valid():
            return Response(
                {
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Invalid search parameters',
                        'details': search_serializer.errors
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            services = ServiceSearchService.search_services(
                location=search_serializer.validated_data.get('location'),
                min_cost=search_serializer.validated_data.get('min_cost'),
                max_cost=search_serializer.validated_data.get('max_cost')
            )
            
            # Paginate results
            paginator = StandardResultsSetPagination()
            paginated_services = paginator.paginate_queryset(services, request)
            serializer = ServiceSerializer(paginated_services, many=True)
            
            return paginator.get_paginated_response(serializer.data)
        
        except ValidationException as e:
            return Response(
                {
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': str(e),
                        'details': e.details
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    elif request.method == 'POST':
        # Create service - only for authenticated service providers
        if not request.user.is_authenticated:
            return Response(
                {
                    'error': {
                        'code': 'AUTHENTICATION_REQUIRED',
                        'message': 'Authentication credentials were not provided.',
                        'details': {}
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if user is a service provider
        if request.user.role != 'PROVIDER':
            return Response(
                {
                    'error': {
                        'code': 'FORBIDDEN',
                        'message': 'Only service providers can create services.',
                        'details': {}
                    }
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        create_serializer = ServiceCreateSerializer(data=request.data)
        
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
            service = ServiceManagementService.create_service(
                provider=request.user,
                name=create_serializer.validated_data['name'],
                description=create_serializer.validated_data['description'],
                location=create_serializer.validated_data['location'],
                cost=create_serializer.validated_data['cost']
            )
            
            return Response(
                {
                    'message': 'Service created successfully',
                    'service': ServiceSerializer(service).data
                },
                status=status.HTTP_201_CREATED
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


@api_view(['GET', 'PUT', 'DELETE'])
def service_detail(request, service_id):
    """
    Retrieve, update, or delete a service.
    
    GET /api/services/{id}/
    
    PUT /api/services/{id}/
    Body: {
        "name": "Updated Name",
        "description": "Updated Description",
        "location": "Updated Location",
        "cost": 150.00
    }
    
    DELETE /api/services/{id}/
    """
    # Get service
    try:
        service = ServiceManagementService.get_service_by_id(service_id)
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
    
    if request.method == 'GET':
        # Retrieve service - available to all users
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        # Update service - only for the service owner
        if not request.user.is_authenticated:
            return Response(
                {
                    'error': {
                        'code': 'AUTHENTICATION_REQUIRED',
                        'message': 'Authentication credentials were not provided.',
                        'details': {}
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        update_serializer = ServiceUpdateSerializer(data=request.data)
        
        if not update_serializer.is_valid():
            return Response(
                {
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Invalid input data',
                        'details': update_serializer.errors
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            updated_service = ServiceManagementService.update_service(
                service=service,
                provider=request.user,
                **update_serializer.validated_data
            )
            
            return Response(
                {
                    'message': 'Service updated successfully',
                    'service': ServiceSerializer(updated_service).data
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
    
    elif request.method == 'DELETE':
        # Delete service - only for the service owner
        if not request.user.is_authenticated:
            return Response(
                {
                    'error': {
                        'code': 'AUTHENTICATION_REQUIRED',
                        'message': 'Authentication credentials were not provided.',
                        'details': {}
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            ServiceManagementService.delete_service(
                service=service,
                provider=request.user
            )
            
            return Response(
                {
                    'message': 'Service deleted successfully'
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


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsServiceProvider])
def my_services(request):
    """
    Get all services for the authenticated provider.
    
    GET /api/services/my-services/
    """
    services = ServiceManagementService.get_provider_services(request.user)
    
    # Paginate results
    paginator = StandardResultsSetPagination()
    paginated_services = paginator.paginate_queryset(services, request)
    serializer = ServiceSerializer(paginated_services, many=True)
    
    return paginator.get_paginated_response(serializer.data)
