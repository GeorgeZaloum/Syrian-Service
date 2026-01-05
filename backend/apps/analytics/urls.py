from django.urls import path
from .views import (
    DashboardMetricsView,
    UserRegistrationStatsView,
    ServiceRequestStatsView,
    ProviderActivityStatsView,
    UserSearchView,
    ProviderSearchView,
    RequestSearchView,
    ExportCSVView
)

urlpatterns = [
    # Dashboard metrics
    path('dashboard/', DashboardMetricsView.as_view(), name='dashboard-metrics'),
    
    # Statistics endpoints
    path('users/registrations/', UserRegistrationStatsView.as_view(), name='user-registration-stats'),
    path('requests/stats/', ServiceRequestStatsView.as_view(), name='request-stats'),
    path('providers/activity/', ProviderActivityStatsView.as_view(), name='provider-activity-stats'),
    
    # Search endpoints
    path('users/search/', UserSearchView.as_view(), name='user-search'),
    path('providers/search/', ProviderSearchView.as_view(), name='provider-search'),
    path('requests/search/', RequestSearchView.as_view(), name='request-search'),
    
    # Export endpoint
    path('export/', ExportCSVView.as_view(), name='export-csv'),
]
