from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authorization.models import CustomUser

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authorization.models import CustomUser, UserLevelMultiplier


@admin.register(UserLevelMultiplier)
class UserLevelMultiplierAdmin(admin.ModelAdmin):
    list_display = ('level', 'multiplier', 'is_active', 'updated_at')
    list_filter = ('is_active', 'level')
    search_fields = ('level',)
    ordering = ('level',)
    
    fieldsets = (
        (None, {
            'fields': ('level', 'multiplier', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of multiplier records to maintain data integrity
        return False


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('telegram_id', 'username', 'first_name', 'last_name', 'user_level', 'get_multiplier_display', 'approved', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'approved', 'user_level')
    search_fields = ('username', 'first_name', 'last_name', 'telegram_id')
    ordering = ('-date_joined',)
    readonly_fields = ('telegram_id', 'get_multiplier_display')

    def get_multiplier_display(self, obj):
        """Display the price multiplier for this user"""
        return f"{obj.get_price_multiplier()}×"
    get_multiplier_display.short_description = 'Price Multiplier'

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': (
                'telegram_id', 'first_name', 'last_name'
            )
        }),
        ('Pricing & Approval', {
            'fields': (
                'user_level', 'get_multiplier_display', 'approved'
            ),
            'description': 'User level multipliers are managed in "User Level Multipliers" section'
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2',
                'telegram_id', 'first_name', 'last_name',
                'user_level', 'approved'
            )
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)