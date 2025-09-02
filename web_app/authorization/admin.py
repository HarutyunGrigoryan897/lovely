from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authorization.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('telegram_id', 'username', 'first_name', 'last_name', 'is_active', 'is_superuser', 'approved', 'date_joined')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'telegram_id')
    ordering = ('username',)
    readonly_fields = ('telegram_id',)

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': (
                'telegram_id', 'first_name', 'last_name'
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
                'telegram_id', 'username', 'first_name', 'last_name'
            )
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)