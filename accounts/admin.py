from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'email', 'first_name', 'last_name',
        'user_type', 'country',
        'is_verified', 'date_joined'
    ]
    list_filter  = ['user_type', 'is_verified', 'country']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('SafariGrants Info', {
            'fields': (
                'user_type', 'phone',
                'country', 'bio',
                'profile_image', 'is_verified'
            )
        }),
    )