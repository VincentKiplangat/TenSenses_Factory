# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Import Django's default UserAdmin
from .models import CustomUser  # Import your CustomUser model


# Create a CustomUserAdmin class that extends Django's UserAdmin
class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed when editing an existing user.
    # We replace 'username' with 'email' as the primary identifier.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Use email for login, and password
        ('Personal info', {'fields': ('first_name', 'last_name')}),  # Your custom personal fields
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Define the fields to be displayed when adding a new user in the admin.
    # This also uses 'email' for creation and includes your custom fields.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password', 'password2'),  # password2 for confirmation
        }),
    )

    # Define the columns to display in the list view of users in the admin.
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')

    # Define filters available in the right sidebar of the user list.
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # Define fields that can be searched in the admin user list.
    search_fields = ('email', 'first_name', 'last_name')

    # Define the default ordering for the user list.
    ordering = ('email',)


# Register your CustomUser model with the custom admin class.
# This tells Django to use CustomUserAdmin when managing CustomUser in the admin interface.
admin.site.register(CustomUser, CustomUserAdmin)
