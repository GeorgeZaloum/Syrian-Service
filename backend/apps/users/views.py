"""
Views for user management and authentication API.
"""
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from core.exceptions import ValidationException, UnauthorizedException
from .models import User, ProviderProfile
from .serializers import (
    UserSerializer,
    RegularUserRegistrationSerializer,
    ServiceProviderRegistrationSerializer,
    PasswordChangeSerializer,
    ProviderProfileSerializer
)
from .services import UserRegistrationService, PasswordChangeService


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Unified registration endpoint that handles both regular users and service providers.
    
    POST /api/auth/register/
    Body: {
        "email": "user@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "role": "REGULAR" | "PROVIDER",
        "service_description": "..." (required if role is PROVIDER)
    }
    """
    role = request.data.get('role')
    
    if not role:
        return Response(
            {
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Role is required',
                    'details': {'role': ['This field is required']}
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if role == 'REGULAR':
        serializer = RegularUserRegistrationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Invalid input data',
                        'details': serializer.errors
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = UserRegistrationService.register_regular_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name']
            )
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    'message': 'Registration successful',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                },
                status=status.HTTP_201_CREATED
            )
        
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
    
    elif role == 'PROVIDER':
        serializer = ServiceProviderRegistrationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Invalid input data',
                        'details': serializer.errors
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user, provider_profile = UserRegistrationService.register_service_provider(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                service_description=serializer.validated_data['service_description']
            )
            
            return Response(
                {
                    'message': 'Provider registration submitted. Your application is pending approval.',
                    'user': UserSerializer(user).data,
                    'provider_profile': ProviderProfileSerializer(provider_profile).data
                },
                status=status.HTTP_201_CREATED
            )
        
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
    
    else:
        return Response(
            {
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid role',
                    'details': {'role': ['Must be either REGULAR or PROVIDER']}
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_regular_user(request):
    """
    Register a new regular user.
    
    POST /api/auth/register/regular/
    """
    serializer = RegularUserRegistrationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid input data',
                    'details': serializer.errors
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = UserRegistrationService.register_regular_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name']
        )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                'message': 'Registration successful',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            },
            status=status.HTTP_201_CREATED
        )
    
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


@api_view(['POST'])
@permission_classes([AllowAny])
def register_service_provider(request):
    """
    Register a new service provider (pending approval).
    
    POST /api/auth/register/provider/
    """
    serializer = ServiceProviderRegistrationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid input data',
                    'details': serializer.errors
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user, provider_profile = UserRegistrationService.register_service_provider(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            service_description=serializer.validated_data['service_description']
        )
        
        return Response(
            {
                'message': 'Provider registration submitted. Your application is pending approval.',
                'user': UserSerializer(user).data,
                'provider_profile': ProviderProfileSerializer(provider_profile).data
            },
            status=status.HTTP_201_CREATED
        )
    
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


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Authenticate user and return JWT tokens.
    
    POST /api/auth/login/
    Body: {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Email and password are required',
                    'details': {}
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Authenticate user
    user = authenticate(request, username=email, password=password)
    
    if user is None:
        return Response(
            {
                'error': {
                    'code': 'AUTHENTICATION_FAILED',
                    'message': 'Invalid email or password',
                    'details': {}
                }
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not user.is_active:
        return Response(
            {
                'error': {
                    'code': 'ACCOUNT_INACTIVE',
                    'message': 'Your account is inactive. Please contact support.',
                    'details': {}
                }
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return Response(
        {
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh(request):
    """
    Refresh access token using refresh token.
    
    POST /api/auth/token/refresh/
    Body: {
        "refresh": "refresh_token_here"
    }
    """
    refresh_token = request.data.get('refresh')
    
    if not refresh_token:
        return Response(
            {
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Refresh token is required',
                    'details': {}
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh = RefreshToken(refresh_token)
        
        return Response(
            {
                'access': str(refresh.access_token),
            },
            status=status.HTTP_200_OK
        )
    
    except Exception as e:
        return Response(
            {
                'error': {
                    'code': 'INVALID_TOKEN',
                    'message': 'Invalid or expired refresh token',
                    'details': {}
                }
            },
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Get current authenticated user profile.
    
    GET /api/auth/me/
    """
    user = request.user
    user_data = UserSerializer(user).data
    
    # Include provider profile if user is a provider
    if user.role == 'PROVIDER':
        try:
            provider_profile = user.provider_profile
            user_data['provider_profile'] = ProviderProfileSerializer(provider_profile).data
        except ProviderProfile.DoesNotExist:
            user_data['provider_profile'] = None
    
    return Response(user_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change user password.
    
    POST /api/auth/password/change/
    Body: {
        "current_password": "old_password",
        "new_password": "new_password"
    }
    """
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    
    if not serializer.is_valid():
        return Response(
            {
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid input data',
                    'details': serializer.errors
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        PasswordChangeService.change_password(
            user=request.user,
            current_password=serializer.validated_data['current_password'],
            new_password=serializer.validated_data['new_password']
        )
        
        return Response(
            {
                'message': 'Password changed successfully. Please login again with your new password.'
            },
            status=status.HTTP_200_OK
        )
    
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



# Provider Approval Views

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_provider_applications(request):
    """
    List all pending provider applications (Admin only).
    
    GET /api/providers/applications/
    """
    # Check if user is admin
    if request.user.role != 'ADMIN':
        return Response(
            {
                'error': {
                    'code': 'FORBIDDEN',
                    'message': 'You do not have permission to access this resource.',
                    'details': {}
                }
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    from .services import ProviderApprovalService
    
    pending_applications = ProviderApprovalService.get_pending_applications()
    serializer = ProviderProfileSerializer(pending_applications, many=True)
    
    return Response(
        {
            'count': pending_applications.count(),
            'results': serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_provider(request, profile_id):
    """
    Approve a provider application (Admin only).
    
    POST /api/providers/applications/{profile_id}/approve/
    """
    # Check if user is admin
    if request.user.role != 'ADMIN':
        return Response(
            {
                'error': {
                    'code': 'FORBIDDEN',
                    'message': 'You do not have permission to perform this action.',
                    'details': {}
                }
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        provider_profile = ProviderProfile.objects.get(id=profile_id)
    except ProviderProfile.DoesNotExist:
        return Response(
            {
                'error': {
                    'code': 'NOT_FOUND',
                    'message': 'Provider profile not found.',
                    'details': {}
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        from .services import ProviderApprovalService
        
        approved_profile = ProviderApprovalService.approve_provider(
            provider_profile=provider_profile,
            admin_user=request.user
        )
        
        return Response(
            {
                'message': 'Provider application approved successfully. Approval email sent.',
                'provider_profile': ProviderProfileSerializer(approved_profile).data
            },
            status=status.HTTP_200_OK
        )
    
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_provider(request, profile_id):
    """
    Reject a provider application (Admin only).
    
    POST /api/providers/applications/{profile_id}/reject/
    """
    # Check if user is admin
    if request.user.role != 'ADMIN':
        return Response(
            {
                'error': {
                    'code': 'FORBIDDEN',
                    'message': 'You do not have permission to perform this action.',
                    'details': {}
                }
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        provider_profile = ProviderProfile.objects.get(id=profile_id)
    except ProviderProfile.DoesNotExist:
        return Response(
            {
                'error': {
                    'code': 'NOT_FOUND',
                    'message': 'Provider profile not found.',
                    'details': {}
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        from .services import ProviderApprovalService
        
        rejected_profile = ProviderApprovalService.reject_provider(
            provider_profile=provider_profile,
            admin_user=request.user
        )
        
        return Response(
            {
                'message': 'Provider application rejected. Rejection email sent.',
                'provider_profile': ProviderProfileSerializer(rejected_profile).data
            },
            status=status.HTTP_200_OK
        )
    
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
