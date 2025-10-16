from django.contrib.auth.models import AbstractUser
from django.db import models


class UserLevel(models.Model):
    """User levels with price multipliers"""
    LEVEL_CHOICES = [
        ('USER', 'User'),
        ('DEALER', 'Dealer'),
        ('VIP', 'VIP'),
        ('PARTNER', 'Partner'),
    ]
    
    name = models.CharField(max_length=20, choices=LEVEL_CHOICES, unique=True)
    multiplier = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=1.8,
        help_text="Price multiplier for this level (e.g., 1.8 means prices are multiplied by 1.8)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['multiplier']
        verbose_name = 'User Level'
        verbose_name_plural = 'User Levels'

    def __str__(self):
        return f"{self.get_name_display()} (×{self.multiplier})"


class CustomUser(AbstractUser):
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    approved = models.BooleanField(default=False)
    user_level = models.ForeignKey(
        UserLevel, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='users',
        help_text="User's pricing level"
    )

    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.username or str(self.telegram_id)
    
    def get_price_multiplier(self):
        """Get the price multiplier for this user"""
        if self.user_level:
            return self.user_level.multiplier
        # Default to USER level multiplier if no level assigned
        default_level = UserLevel.objects.filter(name='USER', is_active=True).first()
        if default_level:
            return default_level.multiplier
        return 1.8  # Fallback to USER default