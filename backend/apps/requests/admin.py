from django.contrib import admin
from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    """Admin interface for ServiceRequest model."""
    
    list_display = ['id', 'service', 'requester', 'provider', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['service__name', 'requester__email', 'provider__email', 'message']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('service', 'requester', 'provider', 'status', 'message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
