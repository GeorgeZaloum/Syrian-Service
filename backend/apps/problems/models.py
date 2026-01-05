from django.db import models
from django.conf import settings


class ProblemReport(models.Model):
    """User-submitted problem with AI recommendations."""
    
    INPUT_TYPE_CHOICES = [
        ('TEXT', 'Text'),
        ('VOICE', 'Voice'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='problem_reports'
    )
    input_type = models.CharField(
        max_length=10,
        choices=INPUT_TYPE_CHOICES,
        default='TEXT'
    )
    problem_text = models.TextField(
        help_text='The problem description (from text input or transcribed from voice)'
    )
    audio_file = models.FileField(
        upload_to='problem_audio/',
        null=True,
        blank=True,
        help_text='Voice recording file (if input_type is VOICE)'
    )
    recommendations = models.JSONField(
        default=list,
        help_text='AI-generated recommendations as a list of solutions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'problem_reports'
        verbose_name = 'Problem Report'
        verbose_name_plural = 'Problem Reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['input_type']),
        ]
    
    def __str__(self):
        return f"Problem by {self.user.email} - {self.input_type} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
