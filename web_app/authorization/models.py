from django.contrib.auth.models import AbstractUser
from django.db import models


class UserLevelMultiplier(models.Model):
    """Model to store price multipliers for each user level"""
    USER_LEVEL_CHOICES = [
        ('user', 'User'),
        ('dealer', 'Dealer'),
        ('vip', 'VIP'),
        ('partner', 'Partner'),
    ]
    
    level = models.CharField(
        max_length=20,
        choices=USER_LEVEL_CHOICES,
        unique=True,
        help_text='User level'
    )
    multiplier = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.00,
        help_text='Price multiplier for this level (e.g., 1.8 for 1.8x prices)'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['level']
        verbose_name = 'User Level Multiplier'
        verbose_name_plural = 'User Level Multipliers'
    
    def __str__(self):
        return f"{self.get_level_display()}: {self.multiplier}x"
    
    @classmethod
    def get_multiplier_for_level(cls, level):
        """Get the multiplier for a specific level"""
        try:
            obj = cls.objects.get(level=level, is_active=True)
            return float(obj.multiplier)
        except cls.DoesNotExist:
            # Fallback to default values if not found
            defaults = {
                'user': 1.8,
                'dealer': 1.7,
                'vip': 1.6,
                'partner': 1.4,
            }
            return defaults.get(level, 1.8)
    
    @classmethod
    def get_default_multiplier(cls):
        """Get the default multiplier (for non-authenticated users or when level is unknown)"""
        return cls.get_multiplier_for_level('user')


class CustomUser(AbstractUser):
    USER_LEVEL_CHOICES = [
        ('user', 'User'),           # Multiplier managed in UserLevelMultiplier model
        ('dealer', 'Dealer'),       # Multiplier managed in UserLevelMultiplier model
        ('vip', 'VIP'),             # Multiplier managed in UserLevelMultiplier model
        ('partner', 'Partner'),     # Multiplier managed in UserLevelMultiplier model
    ]
    
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    approved = models.BooleanField(default=False)
    user_level = models.CharField(
        max_length=20, 
        choices=USER_LEVEL_CHOICES, 
        default='user',
        help_text='User pricing level (hidden from users)'
    )

    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.username or str(self.telegram_id)
    
    def get_price_multiplier(self):
        """Get the price multiplier for this user's level from UserLevelMultiplier model"""
        return UserLevelMultiplier.get_multiplier_for_level(self.user_level)