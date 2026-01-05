"""
Analytics service for aggregating platform metrics and statistics.
"""
from django.db.models import Count, Q, F
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import datetime, timedelta
from apps.users.models import User, ProviderProfile
from apps.services.models import Service
from apps.requests.models import ServiceRequest


class AnalyticsService:
    """Service for calculating analytics metrics and statistics."""
    
    @staticmethod
    def get_dashboard_metrics(start_date=None, end_date=None):
        """
        Get real-time dashboard metrics.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            
        Returns:
            dict: Dashboard metrics including total users, active providers, pending requests
        """
        # Build date filter
        date_filter = Q()
        if start_date:
            date_filter &= Q(created_at__gte=start_date)
        if end_date:
            date_filter &= Q(created_at__lte=end_date)
        
        # Calculate metrics
        total_users = User.objects.filter(date_filter).count()
        total_regular_users = User.objects.filter(date_filter, role='REGULAR').count()
        total_providers = User.objects.filter(date_filter, role='PROVIDER').count()
        
        # Active providers (approved)
        active_providers = ProviderProfile.objects.filter(
            approval_status='APPROVED'
        ).count()
        
        # Pending provider applications
        pending_applications = ProviderProfile.objects.filter(
            approval_status='PENDING'
        ).count()
        
        # Service request metrics
        pending_requests = ServiceRequest.objects.filter(status='PENDING').count()
        accepted_requests = ServiceRequest.objects.filter(status='ACCEPTED').count()
        completed_requests = ServiceRequest.objects.filter(status='COMPLETED').count()
        rejected_requests = ServiceRequest.objects.filter(status='REJECTED').count()
        
        # Total services
        total_services = Service.objects.filter(is_active=True).count()
        
        return {
            'total_users': total_users,
            'total_regular_users': total_regular_users,
            'total_providers': total_providers,
            'active_providers': active_providers,
            'pending_applications': pending_applications,
            'pending_requests': pending_requests,
            'accepted_requests': accepted_requests,
            'completed_requests': completed_requests,
            'rejected_requests': rejected_requests,
            'total_services': total_services,
        }
    
    @staticmethod
    def get_user_registration_stats(start_date=None, end_date=None, role=None):
        """
        Get user registration statistics over time.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            role: Optional role filter (REGULAR, PROVIDER, ADMIN)
            
        Returns:
            list: Daily user registration counts
        """
        queryset = User.objects.all()
        
        # Apply filters
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        if role:
            queryset = queryset.filter(role=role)
        
        # Group by date and count
        stats = queryset.annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        return list(stats)
    
    @staticmethod
    def get_service_request_stats(start_date=None, end_date=None, status=None):
        """
        Get service request statistics over time.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            status: Optional status filter (PENDING, ACCEPTED, REJECTED, COMPLETED)
            
        Returns:
            list: Daily service request counts
        """
        queryset = ServiceRequest.objects.all()
        
        # Apply filters
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        if status:
            queryset = queryset.filter(status=status)
        
        # Group by date and count
        stats = queryset.annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        return list(stats)
    
    @staticmethod
    def get_provider_activity_stats(start_date=None, end_date=None):
        """
        Get provider activity statistics.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            
        Returns:
            list: Provider activity metrics including services and requests
        """
        # Get providers
        providers = User.objects.filter(role='PROVIDER')
        
        if start_date or end_date:
            # Filter providers by creation date
            if start_date:
                providers = providers.filter(created_at__gte=start_date)
            if end_date:
                providers = providers.filter(created_at__lte=end_date)
        
        # Annotate with service and request counts
        provider_stats = providers.annotate(
            services_count=Count('services', filter=Q(services__is_active=True)),
            received_requests_count=Count('received_requests'),
            accepted_requests_count=Count(
                'received_requests',
                filter=Q(received_requests__status='ACCEPTED')
            ),
            completed_requests_count=Count(
                'received_requests',
                filter=Q(received_requests__status='COMPLETED')
            )
        ).values(
            'id',
            'email',
            'first_name',
            'last_name',
            'created_at',
            'services_count',
            'received_requests_count',
            'accepted_requests_count',
            'completed_requests_count'
        ).order_by('-received_requests_count')
        
        return list(provider_stats)
    
    @staticmethod
    def search_users(query, role=None):
        """
        Search users by email or name.
        
        Args:
            query: Search query string
            role: Optional role filter
            
        Returns:
            QuerySet: Filtered users
        """
        queryset = User.objects.all()
        
        if query:
            queryset = queryset.filter(
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        
        if role:
            queryset = queryset.filter(role=role)
        
        return queryset.order_by('-created_at')
    
    @staticmethod
    def search_providers(query):
        """
        Search service providers by email, name, or service description.
        
        Args:
            query: Search query string
            
        Returns:
            QuerySet: Filtered provider profiles
        """
        queryset = ProviderProfile.objects.select_related('user').all()
        
        if query:
            queryset = queryset.filter(
                Q(user__email__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(service_description__icontains=query)
            )
        
        return queryset.order_by('-created_at')
    
    @staticmethod
    def search_requests(query, status=None):
        """
        Search service requests by service name or user details.
        
        Args:
            query: Search query string
            status: Optional status filter
            
        Returns:
            QuerySet: Filtered service requests
        """
        queryset = ServiceRequest.objects.select_related(
            'service',
            'requester',
            'provider'
        ).all()
        
        if query:
            queryset = queryset.filter(
                Q(service__name__icontains=query) |
                Q(requester__email__icontains=query) |
                Q(requester__first_name__icontains=query) |
                Q(requester__last_name__icontains=query) |
                Q(provider__email__icontains=query) |
                Q(provider__first_name__icontains=query) |
                Q(provider__last_name__icontains=query)
            )
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')



class ReportGenerationService:
    """Service for generating CSV reports from analytics data."""
    
    @staticmethod
    def generate_users_csv(start_date=None, end_date=None, role=None):
        """
        Generate CSV report for users.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            role: Optional role filter
            
        Returns:
            list: CSV rows with user data
        """
        users = AnalyticsService.search_users(query='', role=role)
        
        # Apply date filters
        if start_date:
            users = users.filter(created_at__gte=start_date)
        if end_date:
            users = users.filter(created_at__lte=end_date)
        
        # Prepare CSV data
        csv_data = []
        csv_data.append([
            'ID',
            'Email',
            'First Name',
            'Last Name',
            'Role',
            'Is Active',
            'Created At'
        ])
        
        for user in users:
            csv_data.append([
                user.id,
                user.email,
                user.first_name,
                user.last_name,
                user.role,
                'Yes' if user.is_active else 'No',
                user.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return csv_data
    
    @staticmethod
    def generate_providers_csv(start_date=None, end_date=None):
        """
        Generate CSV report for providers.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            
        Returns:
            list: CSV rows with provider data
        """
        providers = AnalyticsService.search_providers(query='')
        
        # Apply date filters
        if start_date:
            providers = providers.filter(created_at__gte=start_date)
        if end_date:
            providers = providers.filter(created_at__lte=end_date)
        
        # Prepare CSV data
        csv_data = []
        csv_data.append([
            'ID',
            'Email',
            'First Name',
            'Last Name',
            'Service Description',
            'Approval Status',
            'Created At',
            'Approved At'
        ])
        
        for provider in providers:
            csv_data.append([
                provider.id,
                provider.user.email,
                provider.user.first_name,
                provider.user.last_name,
                provider.service_description,
                provider.approval_status,
                provider.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                provider.approved_at.strftime('%Y-%m-%d %H:%M:%S') if provider.approved_at else 'N/A'
            ])
        
        return csv_data
    
    @staticmethod
    def generate_requests_csv(start_date=None, end_date=None, status=None):
        """
        Generate CSV report for service requests.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            status: Optional status filter
            
        Returns:
            list: CSV rows with request data
        """
        requests = AnalyticsService.search_requests(query='', status=status)
        
        # Apply date filters
        if start_date:
            requests = requests.filter(created_at__gte=start_date)
        if end_date:
            requests = requests.filter(created_at__lte=end_date)
        
        # Prepare CSV data
        csv_data = []
        csv_data.append([
            'ID',
            'Service Name',
            'Requester Email',
            'Requester Name',
            'Provider Email',
            'Provider Name',
            'Status',
            'Message',
            'Created At',
            'Updated At'
        ])
        
        for request in requests:
            csv_data.append([
                request.id,
                request.service.name,
                request.requester.email,
                request.requester.full_name,
                request.provider.email,
                request.provider.full_name,
                request.status,
                request.message,
                request.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                request.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return csv_data
    
    @staticmethod
    def generate_dashboard_metrics_csv(start_date=None, end_date=None):
        """
        Generate CSV report for dashboard metrics.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            
        Returns:
            list: CSV rows with metrics data
        """
        metrics = AnalyticsService.get_dashboard_metrics(
            start_date=start_date,
            end_date=end_date
        )
        
        # Prepare CSV data
        csv_data = []
        csv_data.append(['Metric', 'Value'])
        
        for key, value in metrics.items():
            # Convert snake_case to Title Case
            metric_name = key.replace('_', ' ').title()
            csv_data.append([metric_name, value])
        
        return csv_data
