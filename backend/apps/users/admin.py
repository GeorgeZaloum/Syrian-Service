from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ProviderProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    """Admin interface for ProviderProfile model."""
    
    list_display = ['user', 'approval_status', 'approved_by', 'approved_at', 'created_at']
    list_filter = ['approval_status', 'created_at', 'approved_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'service_description']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Provider Information', {'fields': ('user', 'service_description')}),
        ('Approval Status', {'fields': ('approval_status', 'approved_by', 'approved_at')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
