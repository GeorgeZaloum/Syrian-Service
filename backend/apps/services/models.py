from django.db import models
from django.core.validators import MinValueValidator
from apps.users.models import User


class Service(models.Model):
    """Service offered by providers."""
    
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='services'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, db_index=True)
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        db_index=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['provider', 'is_active']),
            models.Index(fields=['location', 'cost']),
        ]
    
    def __str__(self):
        return f"{self.name} by {self.provider.full_name}"
    
    def has_pending_requests(self):
        """Check if service has any pending requests."""
        return self.service_requests.filter(status='PENDING').exists()
