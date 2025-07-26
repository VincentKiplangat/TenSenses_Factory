# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager  # <--- ADD THIS IMPORT


class CustomUser(AbstractUser):
    """
    A custom user model that extends Django's AbstractUser.
    - Uses 'email' as the primary authentication field (USERNAME_FIELD).
    - Adds a 'full_name' field for user display.
    - Overrides the default 'email' field to ensure it's unique.
    - Explicitly makes the inherited 'username' field nullable and populates it with email.
    - Uses CustomUserManager for object creation.
    """
    full_name = models.CharField(max_length=255, blank=False, null=False, help_text="Enter your full name.")
    email = models.EmailField(unique=True, verbose_name="email address")

    # Make the default username field from AbstractUser nullable and blank.
    # This prevents conflicts when email is the USERNAME_FIELD.
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)

    USERNAME_FIELD = 'email'  # Set 'email' as the field used for authentication
    REQUIRED_FIELDS = ['full_name']  # These fields will be prompted when creating a superuser

    # IMPORTANT CHANGE: Assign your custom manager to the 'objects' attribute
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        if self.full_name:
            return self.full_name.split(' ')[0]
        return self.email

    # IMPORTANT: Remove the custom `save` method you added previously.
    # The CustomUserManager now handles setting the username based on email during creation.
    # If you keep it, it might cause conflicts or redundant logic.
    # def save(self, *args, **kwargs):
    #     if not self.username and self.email:
    #         self.username = self.email
    #     super().save(*args, **kwargs)
