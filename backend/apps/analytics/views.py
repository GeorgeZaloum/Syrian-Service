"""
Views for analytics endpoints.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date
from core.permissions import IsAdmin
from .services import AnalyticsService
from .serializers import (
    DashboardMetricsSerializer,
    DateCountSerializer,
    ProviderActivitySerializer,
    UserSearchSerializer,
    ProviderSearchSerializer,
    ServiceRequestSearchSerializer
)


class DashboardMetricsView(APIView):
    """
    API endpoint for dashboard metrics.
    GET /api/analytics/dashboard/
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """Get real-time dashboard metrics."""
        # Parse date filters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            start_date = parse_date(start_date)
        if end_date:
            end_date = parse_date(end_date)
        
        # Get metrics
        metrics = AnalyticsService.get_dashboard_metrics(
            start_date=start_date,
            end_date=end_date
        )
        
        serializer = DashboardMetricsSerializer(metrics)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationStatsView(APIView):
    """
    API endpoint for user registration statistics.
    GET /api/analytics/users/registrations/
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """Get user registration statistics over time."""
        # Parse filters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        role = request.query_params.get('role')
        
        if start_date:
            start_date = parse_date(start_date)
        if end_date:
            end_date = parse_date(end_date)
        
        # Validate role
        if role and role not in ['REGULAR', 'PROVIDER', 'ADMIN']:
            return Response(
                {'error': 'Invalid role. Must be REGULAR, PROVIDER, or ADMIN.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get statistics
        stats = AnalyticsService.get_user_registration_stats(
            start_date=start_date,
            end_date=end_date,
            role=role
        )
        
        serializer = DateCountSerializer(stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceRequestStatsView(APIView):
    """
    API endpoint for service request statistics.
    GET /api/analytics/requests/stats/
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """Get service request statistics over time."""
        # Parse filters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        req_status = request.query_params.get('status')
        
        if start_date:
            start_date = parse_date(start_date)
        if end_date:
            end_date = parse_date(end_date)
        
        # Validate status
        if req_status and req_status not in ['PENDING', 'ACCEPTED', 'REJECTED', 'COMPLETED']:
            return Response(
                {'error': 'Invalid status. Must be PENDING, ACCEPTED, REJECTED, or COMPLETED.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get statistics
        stats = AnalyticsService.get_service_request_stats(
            start_date=start_date,
            end_date=end_date,
            status=req_status
        )
        
        serializer = DateCountSerializer(stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProviderActivityStatsView(APIView):
    """
    API endpoint for provider activity statistics.
    GET /api/analytics/providers/activity/
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """Get provider activity statistics."""
        # Parse filters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            start_date = parse_date(start_date)
        if end_date:
            end_date = parse_date(end_date)
        
        # Get statistics
        stats = AnalyticsService.get_provider_activity_stats(
            start_date=start_date,
            end_date=end_date
        )
        
        serializer = ProviderActivitySerializer(stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSearchView(APIView):
    """
    API endpoint for searching users.
    GET /api/analytics/users/search/
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """Search users by email or name."""
        query = request.query_params.get('q', '')
        role = request.query_params.get('role')
        
        # Validate role
        if role and role not in ['REGULAR', 'PROVIDER', 'ADMIN']:
            return Response(
                {'error': 'Invalid role. Must be REGULAR, PROVIDER, or ADMIN.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Search users
        users = AnalyticsService.search_users(query=query, role=role)
        
        # Paginate results
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UserSearchSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = UserSearchSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @property
    def paginator(self):
        """Get paginator instance."""
        if not hasattr(self, '_paginator'):
            from rest_framework.pagination import PageNumberPagination
            self._paginator = PageNumberPagination()
            self._paginator.page_size = 20
        return self._paginator
    
    def paginate_queryset(self, queryset):
        """Paginate queryset."""
        return self.paginator.paginate_queryset(queryset, self.request, view=self)
    
    def get_paginated_response(self, data):
        """Get paginated response."""
        return self.paginator.get_paginated_response(data)


class ProviderSearchView(APIView):
    """
    API endpoint for searching providers.
    GET /api/analytics/providers/search/
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """Search providers by email, name, or service description."""
        query = request.query_params.get('q', '')
        
        # Search providers
        providers = AnalyticsService.search_providers(query=query)
        
        # Paginate results
        page = self.paginate_queryset(providers)
        if page is not None:
            serializer = ProviderSearchSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProviderSearchSerializer(providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @property
    def paginator(self):
        """Get paginator instance."""
        if not hasattr(self, '_paginator'):
            from rest_framework.pagination import PageNumberPagination
            self._paginator = PageNumberPagination()
            self._paginator.page_size = 20
        return self._paginator
    
    def paginate_queryset(self, queryset):
        """Paginate queryset."""
        return self.paginator.paginate_queryset(queryset, self.request, view=self)
    
    def get_paginated_response(self, data):
        """Get paginated response."""
        return self.paginator.get_paginated_response(data)


class RequestSearchView(APIView):
    """
    API endpoint for searching service requests.
    GET /api/analytics/requests/search/
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """Search service requests by service name or user details."""
        query = request.query_params.get('q', '')
        req_status = request.query_params.get('status')
        
        # Validate status
        if req_status and req_status not in ['PENDING', 'ACCEPTED', 'REJECTED', 'COMPLETED']:
            return Response(
                {'error': 'Invalid status. Must be PENDING, ACCEPTED, REJECTED, or COMPLETED.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Search requests
        requests = AnalyticsService.search_requests(query=query, status=req_status)
        
        # Paginate results
        page = self.paginate_queryset(requests)
        if page is not None:
            serializer = ServiceRequestSearchSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ServiceRequestSearchSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @property
    def paginator(self):
        """Get paginator instance."""
        if not hasattr(self, '_paginator'):
            from rest_framework.pagination import PageNumberPagination
            self._paginator = PageNumberPagination()
            self._paginator.page_size = 20
        return self._paginator
    
    def paginate_queryset(self, queryset):
        """Paginate queryset."""
        return self.paginator.paginate_queryset(queryset, self.request, view=self)
    
    def get_paginated_response(self, data):
        """Get paginated response."""
        return self.paginator.get_paginated_response(data)



class ExportCSVView(APIView):
    """
    API endpoint for exporting analytics data as CSV.
    GET /api/analytics/export/
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """Export analytics data as CSV file."""
        import csv
        from django.http import HttpResponse
        from .services import ReportGenerationService
        
        # Get export type
        export_type = request.query_params.get('type', 'users')
        
        # Parse date filters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            start_date = parse_date(start_date)
        if end_date:
            end_date = parse_date(end_date)
        
        # Generate CSV data based on type
        if export_type == 'users':
            role = request.query_params.get('role')
            if role and role not in ['REGULAR', 'PROVIDER', 'ADMIN']:
                return Response(
                    {'error': 'Invalid role. Must be REGULAR, PROVIDER, or ADMIN.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            csv_data = ReportGenerationService.generate_users_csv(
                start_date=start_date,
                end_date=end_date,
                role=role
            )
            filename = 'users_report.csv'
        
        elif export_type == 'providers':
            csv_data = ReportGenerationService.generate_providers_csv(
                start_date=start_date,
                end_date=end_date
            )
            filename = 'providers_report.csv'
        
        elif export_type == 'requests':
            req_status = request.query_params.get('status')
            if req_status and req_status not in ['PENDING', 'ACCEPTED', 'REJECTED', 'COMPLETED']:
                return Response(
                    {'error': 'Invalid status. Must be PENDING, ACCEPTED, REJECTED, or COMPLETED.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            csv_data = ReportGenerationService.generate_requests_csv(
                start_date=start_date,
                end_date=end_date,
                status=req_status
            )
            filename = 'requests_report.csv'
        
        elif export_type == 'metrics':
            csv_data = ReportGenerationService.generate_dashboard_metrics_csv(
                start_date=start_date,
                end_date=end_date
            )
            filename = 'metrics_report.csv'
        
        else:
            return Response(
                {'error': 'Invalid export type. Must be users, providers, requests, or metrics.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        for row in csv_data:
            writer.writerow(row)
        
        return response
