from django.contrib.admin import register as admin_register
from django.contrib.auth.admin import UserAdmin

from .models import User as UserModel


@admin_register(UserModel)
class CustomUserAdmin(UserAdmin):
    """Default User Admin"""
    fieldsets = UserAdmin.fieldsets + (
        (
            'Additional info',
            {
                'fields': (
                    'nickname',
                    'bio',
                    'profile_image',
                    'thumbnail_image',
                    'language',
                    'superuser',
                    'login_method',
                ),
            }
        ),
    )
    list_display = UserAdmin.list_display + (
        'language',
        'superuser',
        'is_active',
        'is_superuser',
        'email_verified',
        'email_secret',
        'login_method',
    )
    ordering = ('-is_superuser', '-is_staff',)
    list_filter = UserAdmin.list_filter + (
        'superuser',
    )
