# your_project_name/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import Django's built-in LoginView and LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),

    # Define the login path explicitly using Django's LoginView
    # Point it to your custom template: accounts/login.html
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # Define the logout path explicitly using Django's LogoutView
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Include Django's built-in authentication URLs for password reset
    # This will provide 'password_reset', 'password_reset_done', etc.
    # Note: We've handled login/logout separately above.
    path('accounts/', include('django.contrib.auth.urls')),

    # Include your custom accounts app URLs (for 'register' and any other custom views)
    path('accounts/', include('accounts.urls')),

    path('', include('inventory.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)