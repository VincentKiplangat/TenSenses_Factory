# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib import messages  # For displaying success/error messages
from django.contrib.auth import login, authenticate, logout  # Django auth functions
from django.contrib.auth.decorators import login_required  # For protecting views (e.g., logout)
from django.contrib.auth import get_user_model  # To get your custom user model

from .forms import CustomUserCreationForm, CustomAuthenticationForm  # Import your custom forms

# Get your custom user model, which is necessary for `authenticate` if you override it
User = get_user_model()


def register_user(request):
    """
    Handles user registration.
    - On GET: Displays a blank registration form.
    - On POST: Processes the submitted registration form.
        - If valid: Saves the user, logs them in, displays a success message, and redirects.
        - If invalid: Displays errors and re-renders the form.
    """
    if request.method == 'POST':
        # Create a form instance from the submitted data
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user and get the user object
            user = form.save()

            # Log the user in immediately after successful registration
            login(request, user)

            # Display a success message
            messages.success(request, f"Welcome, {user.full_name}! Your account has been created successfully.")

            # Redirect to your desired post-registration page (e.g., inventory dashboard)
            # Make sure 'inventory_home' is a valid URL name in your inventory/urls.py
            return redirect('inventory_home')
        else:
            # If the form is not valid, iterate through errors and display them
            for field, errors in form.errors.items():
                for error in errors:
                    # Format field names for better readability (e.g., "full_name" to "Full Name")
                    field_name = field.replace('_', ' ').title() if field != '__all__' else "General Error"
                    messages.error(request, f"{field_name}: {error}")
            messages.error(request, "Please correct the errors below to complete registration.")
    else:
        # For GET requests, create a new blank form instance to display
        form = CustomUserCreationForm()

    # Render the registration template, passing the form context
    return render(request, 'accounts/register.html', {'form': form})


def login_user(request):
    """
    Handles user login.
    - On GET: Displays the login form.
    - On POST: Processes submitted login credentials.
        - If valid: Authenticates user, logs them in, displays success, and redirects.
        - If invalid: Displays error messages.
    """
    # If the user is already authenticated, redirect them to the home page
    if request.user.is_authenticated:
        return redirect('inventory_home')

    if request.method == 'POST':
        # Create a form instance from the submitted data
        # AuthenticationForm requires 'request' as its first argument
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # AuthenticationForm uses 'username' for the identifier.
            # Since our CustomUser uses 'email' as USERNAME_FIELD, this will be the email.
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user. Django's authenticate uses the USERNAME_FIELD by default.
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)  # Log the user into the session
                messages.success(request, f"Welcome back, {user.full_name or user.email}!")
                # Redirect to the 'next' URL (if provided in the query string) or default home
                return redirect(request.GET.get('next', 'inventory_home'))
            else:
                messages.error(request, "Invalid email or password.")
        else:
            # If the form itself is invalid (e.g., empty fields)
            messages.error(request, "Invalid email or password. Please check your credentials.")
    else:
        # For GET requests, create a new blank form instance
        form = CustomAuthenticationForm()

    # Render the login template with the form
    return render(request, 'accounts/login.html', {'form': form})


@login_required  # This decorator ensures only logged-in users can access this view
def logout_user(request):
    """
    Logs out the current user and redirects to the login page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    # Redirect to the login page after logout. 'login' is the URL name for our login view.
    return redirect('login')