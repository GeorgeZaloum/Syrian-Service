from django.urls import path
from . import views

urlpatterns = [
    # Unified registration endpoint
    path('register/', views.register, name='register'),
    
    # Legacy registration endpoints (kept for backward compatibility)
    path('register/regular/', views.register_regular_user, name='register-regular-user'),
    path('register/provider/', views.register_service_provider, name='register-service-provider'),
    
    # Authentication endpoints
    path('login/', views.login, name='login'),
    path('token/refresh/', views.token_refresh, name='token-refresh'),
    path('me/', views.current_user, name='current-user'),
    
    # Password management
    path('password/change/', views.change_password, name='change-password'),
    
    # Provider approval endpoints (Admin only)
    path('providers/applications/', views.list_provider_applications, name='list-provider-applications'),
    path('providers/applications/<int:profile_id>/approve/', views.approve_provider, name='approve-provider'),
    path('providers/applications/<int:profile_id>/reject/', views.reject_provider, name='reject-provider'),
]
