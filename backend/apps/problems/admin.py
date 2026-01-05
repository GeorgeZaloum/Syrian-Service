from django.contrib import admin
from .models import ProblemReport


@admin.register(ProblemReport)
class ProblemReportAdmin(admin.ModelAdmin):
    """Admin interface for ProblemReport model."""
    
    list_display = ['id', 'user', 'input_type', 'problem_text_preview', 'created_at']
    list_filter = ['input_type', 'created_at']
    search_fields = ['user__email', 'problem_text']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Problem Details', {
            'fields': ('input_type', 'problem_text', 'audio_file')
        }),
        ('AI Recommendations', {
            'fields': ('recommendations',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def problem_text_preview(self, obj):
        """Show a preview of the problem text."""
        if len(obj.problem_text) > 50:
            return f"{obj.problem_text[:50]}..."
        return obj.problem_text
    
    problem_text_preview.short_description = 'Problem Preview'
