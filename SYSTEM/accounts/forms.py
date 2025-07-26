# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm # Ensure UserChangeForm is imported
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Import your CustomUser model from accounts/models.py
from .models import CustomUser # Ensure CustomUser is imported for CustomUserChangeForm

# Get your custom user model
User = get_user_model()


# --- Custom User Forms ---

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating new users.
    - Inherits from Django's UserCreationForm.
    - Includes 'full_name' and 'email' fields, making 'email' required.
    - Adds custom validation for the email domain (@tensenses.com) and uniqueness.
    """
    full_name = forms.CharField(
        max_length=255,
        required=True,
        help_text='Required. Your full name (e.g., Purity Kasyoka).',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'})
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Must be a @tensenses.com email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Fields to display in the registration form
        fields = ('full_name', 'email', 'password', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove the default 'username' field, as our CustomUser uses 'email' as USERNAME_FIELD
        if 'username' in self.fields:
            del self.fields['username']

        # Apply 'form-control' class to all other fields for consistent styling
        # This loop ensures all fields get the 'form-control' class
        for field_name, field in self.fields.items():
            # Exclude password fields as they are styled specifically below
            if field_name not in ['password', 'password2']:
                field.widget.attrs.update({'class': 'form-control rounded-md'})

        # Apply 'form-control' Bootstrap class to password fields specifically
        # These will override the general loop if 'rounded-md' is not desired for passwords
        if 'password' in self.fields:
            self.fields['password'].widget.attrs['class'] = 'form-control'
            self.fields['password'].widget.attrs['placeholder'] = 'Password'
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@tensenses.com'):
            raise ValidationError("Only @tensenses.com email addresses are allowed for registration.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email address is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    A custom form for user authentication (login).
    - Inherits from Django's AuthenticationForm.
    - Renames the default 'username' field label to 'Email Address' for clarity.
    - Applies Bootstrap 'form-control' class to input fields.
    """
    username = forms.CharField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass


class CustomUserChangeForm(UserChangeForm):
    """
    A custom form for changing user details in the admin, extending Django's UserChangeForm.
    It includes full_name field.
    """
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'full_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
