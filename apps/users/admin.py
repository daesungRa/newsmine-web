from django.contrib.admin import register as admin_register
from django.contrib.auth.admin import UserAdmin

from .models import User as UserModel


@admin_register(UserModel)
class CustomUserAdmin(UserAdmin):
    """Default User Admin"""
    fieldsets = UserAdmin.fieldsets
    list_display = UserAdmin.list_display
    ordering = ('-is_superuser', '-is_staff',)
    list_filter = UserAdmin.list_filter
