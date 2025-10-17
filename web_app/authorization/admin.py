from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authorization.models import CustomUser, UserLevel


@admin.register(UserLevel)
class UserLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'multiplier', 'is_active', 'user_count', 'updated_at')
    list_filter = ('is_active', 'name')
    search_fields = ('name',)
    ordering = ('multiplier',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'multiplier', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def user_count(self, obj):
        """Display the number of users with this level"""
        return obj.users.count()
    user_count.short_description = 'Users Count'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('telegram_id', 'username', 'first_name', 'last_name', 'user_level', 'is_active', 'is_superuser', 'approved', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'user_level', 'approved')
    search_fields = ('username', 'first_name', 'last_name', 'telegram_id')
    ordering = ('username',)
    # readonly_fields = ('telegram_id',)

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': (
                'telegram_id', 'first_name', 'last_name', 'user_level'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'approved',
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
                'telegram_id', 'username', 'first_name', 'last_name', 'user_level'
            )
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)